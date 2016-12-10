# -*- coding: utf-8 -*-
import os
import logging
import time
from collections import namedtuple

from slackclient import SlackClient

from .resolver import resolve


BOT_ID = os.environ.get('SLACK_BOT_ID', 'U3BMAJT2A')
SLACK_TOKEN = os.environ.get('SLACK_CHOBOI_API_TOKEN')

DEFAULT_RESPONSE = "Sorry, I don't understand"
READ_WEBSOCKET_DELAY = 1

logger = logging.getLogger(__name__)


class SlackEvents:
    Message = namedtuple('Message', ['command', 'channel', 'user'])
    Error = namedtuple('Error', ['error', 'code', 'msg'])


class Bot:

    at_bot = "<@{}>".format(BOT_ID)
    resolved_commands = []
    default_channel = "#general"

    def __init__(self):
        # just slack for now
        self.client = SlackClient(SLACK_TOKEN)

    def connect(self):
        """
        Connect to bot client
        """
        if not self.client.rtm_connect():
            raise Exception()
        logger.info("Bot connected")
        while True:
            self._listen()
            self._respond()
            time.sleep(READ_WEBSOCKET_DELAY)

    def _listen(self):
        """
        Append slack output to the shared output queue
        """
        output_list = self.client.rtm_read()
        if output_list and len(output_list) == 0:
            return output_list

        commands = self.__process_output(output_list)
        self.resolved_commands.extend(commands)

    def _respond(self):
        """
        TODO : RTM?
        """
        # TODO one at a time
        while self.resolved_commands:
            output = self.resolved_commands.pop()
            if isinstance(output, SlackEvents.Error):
                self.__respond_with_error(output)
            else:
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

    def __process_output(self, output_list):
        """
        process output

        TODO output list content should be one type
        """
        resolved = []
        for output in output_list:
            if not output:
                continue

            sanitized = None
            if output.get('type') == 'error':
                sanitized = self.__process_error(output)
            elif output.get('type') == 'message':
                sanitized = self.__process_message(output)
            else:
                logger.info("Processing unhandled: {}".format(output))

            if sanitized:
                resolved.append(sanitized)

        return resolved

    def __process_error(self, output):
        """
        Process error event
        """
        logger.error("Processing error: {}".format(output))
        return SlackEvents.Error(
            error=output.get('error'),
            code=output.get('code'),
            msg=output.get('msg')
        )

    def __process_message(self, output):
        """
        Process message event
        """
        logger.info("Processing message: {}".format(output))
        text = output.get('text', '').strip().lower()
        command = resolve(text, at=self.at_bot)
        if command:
            return SlackEvents.Message(
                command=command,
                channel=output.get('channel', self.default_channel),
                user=output.get('user')
            )

    def __respond_with_error(self, output):
        """
        Respond with error
        """
        self.client.api_call(
            "chat.postMessage",
            channel="#choboi-errors",
            text="{}".format(output),
            as_user=True
        )
