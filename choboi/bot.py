# -*- coding: utf-8 -*-
import os
import time
from collections import namedtuple

from slackclient import SlackClient

from .resolver import resolve


BOT_ID = 'U3BMAJT2A'
AT_BOT = "<@{}>".format(BOT_ID)
SLACK_TOKEN = os.environ.get('SLACK_CHOBOI_API_TOKEN')
DEFAULT_RESPONSE = "Sorry, I don't understand"
READ_WEBSOCKET_DELAY = 1

ClientOutput = namedtuple('ClientOutput', ['command', 'destination'])


class Bot:

    def __init__(self):
        # just slack for now
        self.client = SlackClient(SLACK_TOKEN)

    def connect(self):
        """
        Connect to bot client
        """
        if not self._connect():
            raise ConnectionError()
        print("Connected!")
        while True:
            try:
                output = self._listen()
                if output:
                    self._respond(output)
                time.sleep(READ_WEBSOCKET_DELAY)
            except Exception as ex:
                print(ex)

    def parse_output(self):
        # hard coded to slack for now
        slack_rtm_output = self.client.rtm_read()
        output_list = slack_rtm_output
        if output_list and len(output_list) > 0:
            for output in output_list:
                if output and 'text' in output and AT_BOT in output['text']:
                    return (
                        output['text'].split(AT_BOT)[1].strip().lower(),
                        output['channel']
                    )
        return None, None

    def _respond(self, output):
        # slack
        if not output.command:
            response = DEFAULT_RESPONSE
        else:
            response = output.command.action(
                *output.command.args,
                **output.command.kwargs
            )
        self.client.api_call(
            "chat.postMessage",
            channel=output.destination,
            text=response,
            as_user=True
        )

    def _listen(self):
        # hard coded to slack for now
        text, channel = self.parse_output()
        if text and channel:
            command = resolve(text)
            return ClientOutput(command=command, destination=channel)

    def _connect(self):
        # Hard code to slack for now
        return self.client.rtm_connect()
