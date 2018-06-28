# -*- coding: utf-8 -*-
import os
import logging
import time
import threading
import queue
from collections import namedtuple

import schedule
import websocket
from slackclient import SlackClient

from . import config
from . import actions
from .resolver import resolve
from .event import events

logger = logging.getLogger(__name__)


class SlackEvent:
    Message = namedtuple('Message', ['command', 'channel', 'user'])
    Error = namedtuple('Error', ['error', 'code', 'msg'])


class Bot:
    default_channel = config.DEFAULT_CHANNEL
    num_writers = 2
    num_listeners = 1
    num_event_watchers = 1
    keep_alive = True

    def __init__(self):
        self.id = config.BOT_ID
        self.client = SlackClient(config.SLACK_TOKEN)
        self.responses = queue.LifoQueue()
        self.threads = []
        self.write_delay = config.WRITE_DELAY
        self.read_delay = config.READ_WEBSOCKET_DELAY
        self.event_delay = 1

    @property
    def at_bot(self):
        return "<@{}>".format(self.id)

    def connect(self):
        """
        Connect to bot client
        """
        if not self.client.rtm_connect(auto_reconnect=True):
            raise Exception("Unable to connect to slack RTM service")
        logger.info("Bot connected")
        self.__respond_with_error("Bot connected")

        done = False
        while not done:
            self.keep_alive = True
            try:
                for i in range(self.num_listeners):
                    self.threads.append(threading.Thread(target=self._listen))
                for i in range(self.num_writers):
                    self.threads.append(threading.Thread(target=self._respond))
                for i in range(self.num_event_watchers):
                    self.threads.append(threading.Thread(target=self._schedule_events))
                for thread in self.threads:
                    thread.start()
            except Exception as ex:
                logging.error("Error occurred: {}".format(ex))
                self.keep_alive = False

            for t in self.threads:
                try:
                    if t.is_alive():
                        t.join()
                except (KeyboardInterrupt, SystemExit):
                    logging.info('Received keyboard interrupt, quitting threads')
                    self.keep_alive = False
                    done = True

    def _schedule_events(self):
        """
        Schedule events and output event result to the output queue
        """
        for e in events:
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
            self.__respond_with_event(event)
        return __process

    def _listen(self):
        """
        Append slack output to the shared output queue
        """
        while self.keep_alive:
            time.sleep(self.read_delay)
            try:
                input_list = self.client.rtm_read()
                if input_list and len(input_list) == 0:
                    continue
                commands = self.__process_input(input_list)
                for command in commands:
                    self.responses.put_nowait(command)
            except Exception as ex:
                logging.error("_listen exception: {}".format(ex))

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
            logger.info("Processing unhandled: {}".format(slack_input))
        return sanitized

    def __process_error(self, slack_input):
        """
        Process error event
        """
        logger.error("Processing error: {}".format(slack_input))
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
        logger.info("Processing message: {}".format(slack_input))
        text = slack_input.get('text', '').strip().lower()
        if text:
            command = resolve(text, at=self.at_bot)
            if command:
                return SlackEvent.Message(
                    command=command,
                    channel=slack_input.get('channel', self.default_channel),
                    user=slack_input.get('user')
                )

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
                    self.__respond_with_error(output)
                else:
                    self.__respond_with_command(output)
            except Exception as ex:
                logging.error("_respond exception: {}".format(ex))

    def __respond_with_error(self, output):
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
        response = output.command.action(
            *output.command.args,
            message=output
        )
        logging.info("Responding '{}'".format(response))
        self.client.api_call(
            "chat.postMessage",
            channel=output.channel,
            text=response,
            as_user=True
        )

    def __respond_with_event(self, event):
        response = event.action()
        if response:
            logging.info(f'Responding {response}')
            self.client.api_call(
                "chat.postMessage",
                channel=event.channel,
                text=response,
                as_user=True
            )
