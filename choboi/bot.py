# -*- coding: utf-8 -*-
import os
import logging
import time
import threading
import queue
from collections import namedtuple

import websocket
from slackclient import SlackClient

from . import config
from . import actions
from .resolver import resolve

logger = logging.getLogger(__name__)


class SlackEvent:
    Message = namedtuple('Message', ['command', 'channel', 'user'])
    Error = namedtuple('Error', ['error', 'code', 'msg'])


class Bot:
    default_channel = "#general"
    num_writers = 2
    num_listeners = 1

    def __init__(self):
        self.id = config.BOT_ID
        self.client = SlackClient(config.SLACK_TOKEN)
        self.resolved_commands = queue.LifoQueue()
        self.threads = []
        self.write_delay = config.WRITE_DELAY
        self.read_delay = config.READ_WEBSOCKET_DELAY

    @property
    def at_bot(self):
        return "<@{}>".format(self.id)

    def connect(self):
        """
        Connect to bot client
        """
        if not self.client.rtm_connect():
            raise Exception("Unable to connect to slack RTM service")
        logger.info("Bot connected")
        self.__respond_with_error("Bot connected")
        try:
            for i in range(self.num_listeners):
                self.threads.append(threading.Thread(target=self._listen))
            for i in range(self.num_writers):
                self.threads.append(threading.Thread(target=self._respond))
            for thread in self.threads:
                thread.start()
        except Exception as ex:
            # Log error and attempt another connection
            logging.error("Error occurred: {}".format(ex))
            self.resolved_commands.join()
            self.connect()
        else:
            self.resolved_commands.join()

    def _listen(self):
        """
        Append slack output to the shared output queue
        """
        while True:
            time.sleep(self.read_delay)
            try:
                input_list = self.client.rtm_read()
                if input_list and len(input_list) == 0:
                    continue

                commands = self.__process_input(input_list)
                for command in commands:
                    self.resolved_commands.put_nowait(command)
            except websocket.WebSocketException as ex:
                logging.error("_listen connection error: {}".format(ex))
                self.__respond_with_error("connection died, attempting to reconnect")
                # let connect() reconnect
                raise
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

    def __process_error(self, output):
        """
        Process error event
        """
        logger.error("Processing error: {}".format(output))
        return SlackEvent.Error(
            error=output.get('error'),
            code=output.get('code'),
            msg=output.get('msg')
        )

    def __process_message(self, output):
        """
        Process message event.  If the output message resolves to a registered command,
        it will return a SlackEvent.Message object which contains the command to perform,
        channel to output the command result, and information about the user who made such
        request.
        """
        logger.info("Processing message: {}".format(output))
        text = output.get('text', '').strip().lower()
        if text:
            command = resolve(text, at=self.at_bot)
            if command:
                return SlackEvent.Message(
                    command=command,
                    channel=output.get('channel', self.default_channel),
                    user=output.get('user')
                )

    def _respond(self):
        """
        Outputs response to slack
        """
        while True:
            time.sleep(self.write_delay)
            try:
                if self.resolved_commands.empty():
                    continue
                output = self.resolved_commands.get()
                if isinstance(output, SlackEvent.Error):
                    self.__respond_with_error(output)
                else:
                    self.__respond_with_message(output)
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

    def __respond_with_message(self, output):
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
