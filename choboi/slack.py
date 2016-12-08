# -*- coding: utf-8 -*-
import os
import time
from slackclient import SlackClient

BOT_ID = 'U3BMAJT2A'
SLACK_TOKEN = os.environ.get('SLACK_CHOBOI_API_TOKEN')

AT_BOT = "<@{}>".format(BOT_ID)


def respond(response, channel):
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response,
        as_user=True
    )


def parse_slack_output(slack_rtm_output):
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return (
                    output['text'].split(AT_BOT)[1].strip().lower(),
                    output['channel']
                )
    return None, None
