# -*- coding: utf-8 -*-
import logging
import time
import threading
import queue
from collections import namedtuple

import markovify
import schedule
from slackclient import SlackClient

from . import storage
from .messages import get_message_text
from .event import events
from .resolver import resolve, Command, static_response

from . import actions # pylint: disable=unused-import

logger = logging.getLogger(__name__)


class SlackEvent:
    Message = namedtuple('Message', ['command', 'channel', 'user'])
    Error = namedtuple('Error', ['error', 'code', 'msg'])



class Bot:
    default_channel = config.DEFAULT_CHANNEL
    num_writers = 2
    num_listeners = 1
    num_event_watchers = 1
    num_markov_trainers = 1 if config.MARKOV_ENABLED else 0
    keep_alive = True

    def __init__(self):
        self.id = config.BOT_ID
        self.client = SlackClient(config.SLACK_TOKEN)
        self.responses = queue.LifoQueue()
        self.threads = []
        self.write_delay = config.WRITE_DELAY
        self.read_delay = config.READ_WEBSOCKET_DELAY
        self.event_delay = 1
        self.model = None
        self.messages = queue.LifoQueue()
        self.storage = None

    @property
    def at_bot(self):
        return "<@{}>".format(self.id)

    def connect(self):
        """
        Connect to bot client
        """
        if config.MARKOV_ENABLED:
            logger.info("training models")
            self._init_models()

        if not self.client.rtm_connect(auto_reconnect=True):
            logger.exception("unable to connect to slack RTM service")
            raise Exception("Unable to connect to slack RTM service")
        logger.info("Bot connected")
        self._respond_to_debug_slack("Bot connected")

        done = False
        while not done:
            self.keep_alive = True
            try:
                for _ in range(self.num_listeners):
                    self.threads.append(threading.Thread(target=self._listen))
                for _ in range(self.num_writers):
                    self.threads.append(threading.Thread(target=self._respond))
                for _ in range(self.num_markov_trainers):
                    self.threads.append(threading.Thread(target=self._train))
                for _ in range(self.num_event_watchers):
                    self.threads.append(threading.Thread(target=self._schedule_events))
                for thread in self.threads:
                    thread.start()
            except Exception as ex:
                logging.error("Error occurred: %s", ex)

            for t in self.threads:
                try:
                    if t.is_alive():
                        t.join()
                except (KeyboardInterrupt, SystemExit):
                    logging.info('Received keyboard interrupt, quitting threads')
                    self.keep_alive = False
                    done = True

    def _init_models(self):
        # TODO config
        self.storage = storage.JSONStorage('data.json')
        message_objs = self.storage.get_messages()
        messages = get_message_text(message_objs)
        if messages:
            self.model = markovify.Text(". ".join(messages), state_size=4)

    def _train(self):
        """
        periodically train markov model
        """
        schedule.every(config.MARKOV_TRAIN_FREQUENCY).seconds.do(self.__train)

    def __train(self):
        try:
            logger.info("begin training models")
            message_objs = []
            size = self.messages.qsize()
            if not size:
                logger.info("no new messages to train with")
                return

            ii = 0
            while ii < size or not self.messages.empty():
                message_objs.append(self.messages.get())
                ii += 1
            messages = get_message_text(message_objs)
            logger.info("collected %d messages", ii)

            model = markovify.Text(". ".join(messages), state_size=4)
            self.model = markovify.combine([model, self.model])
            logger.info("trained %d new messages", ii)

            self.storage.save_messages(message_objs)
            logger.info("saving %d new messages", ii)
        except Exception:
            logger.exception('something failed while training choboi')

    def _schedule_events(self):
        """
        Schedule events and output event result to the output queue
        """
        for e in events:
            if e.at:
                schedule.every().day.at(e.at).do(
                    self.__process_event(e)
                )
            else:
                schedule.every(e.frequency).seconds.do(
                    self.__process_event(e)
                )
        while self.keep_alive:
            time.sleep(self.event_delay)
            schedule.run_pending()

    def __process_event(self, event):
        """
        process an event
        """
        def __process():
            try:
                self.__respond_with_event(event)
            except Exception:
                logger.error('failed to process event %s', event)
        return __process

    def _listen(self):
        """
        Append slack output to the shared output queue
        """
        while self.keep_alive:
            time.sleep(self.read_delay)
            try:
                input_list = self.client.rtm_read()
                if input_list and not input_list:
                    continue
                commands = self.__process_input(input_list)
                for command in commands:
                    self.responses.put_nowait(command)
            except Exception as ex:
                logging.error("_listen exception: %s", ex)

    def __process_input(self, input_list):
        """
        process input from slack
        """
        resolved = []
        for slack_input in input_list:
            # If the input is empty, just skip the rest
            if not slack_input:
                continue

            # sanitize the input to a format we understand
            sanitized = self.__sanitize_input(slack_input)
            if sanitized:
                resolved.append(sanitized)

        return resolved

    def __sanitize_input(self, slack_input):
        """
        Sanitizes raw marshaled slack_input JSON into one of SlackEvent.Error or SlackEvent.Message
        """
        sanitized = None
        if slack_input.get('type') == 'error':
            sanitized = self.__process_error(slack_input)
        elif slack_input.get('type') == 'message':
            if slack_input.get('user') != self.id:
                sanitized = self.__process_message(slack_input)
        else:
            logger.info("Processing unhandled: %s", slack_input)
        return sanitized

    def __process_error(self, slack_input):
        """
        Process error event
        """
        logger.error("Processing error: %s", slack_input)
        return SlackEvent.Error(
            error=slack_input.get('error'),
            code=slack_input.get('code'),
            msg=slack_input.get('msg')
        )

    def __process_message(self, slack_input):
        """
        Process message event.  If the slack_input message resolves to a registered command,
        it will return a SlackEvent.Message object which contains the command to perform,
        channel to output the command result, and information about the user who made such
        request.
        """
        logger.info("Processing message: %s", slack_input)
        text = slack_input.get('text', '').strip().lower()
        handle_default = not config.MARKOV_ENABLED

        if config.MARKOV_ENABLED:
            try:
                self.messages.put_nowait(slack_input)
            except Exception:
                logger.exception("failed to put message in the message queue")

        if text:
            command = resolve(text, at=self.at_bot, handle_default=handle_default)
            if command:
                return SlackEvent.Message(
                    command=command,
                    channel=slack_input.get('channel', self.default_channel),
                    user=slack_input.get('user')
                )
            if self.at_bot.lower() in text and not handle_default:
                message = self.model.make_short_sentence(100, tries=50)
                return SlackEvent.Message(
                    command=Command(action=static_response(message), args=[]),
                    channel=slack_input.get('channel', self.default_channel),
                    user=slack_input.get('user')
                )
        return None

    def _respond(self):
        """
        Outputs response to slack
        """
        while self.keep_alive:
            time.sleep(self.write_delay)
            try:
                if self.responses.empty():
                    continue
                output = self.responses.get()
                if isinstance(output, SlackEvent.Error):
                    self._respond_to_debug_slack(output)
                else:
                    self.__respond_with_command(output)
            except Exception as ex:
                logging.error("_respond exception: %s", ex)

    def _respond_to_debug_slack(self, output):
        """
        Respond with error
        """
        self.client.api_call(
            "chat.postMessage",
            channel="#choboi-logs",
            text="{}".format(output),
            as_user=True
        )

    def __respond_with_command(self, output):
        """
        Apply command action and reply with a message
        """
        # TODO: use a context object
        response = output.command.action(
            *output.command.args,
            message=output,
            user=output.user,
        )
        logging.info("Responding %s", response)
        self.client.api_call(
            "chat.postMessage",
            channel=output.channel,
            text=response,
            as_user=True
        )

    def __respond_with_event(self, event):
        response = event.action()
        if response:
            logging.info('Responding %s')
            self.client.api_call(
                "chat.postMessage",
                channel=event.channel,
                text=response,
                as_user=True
            )
