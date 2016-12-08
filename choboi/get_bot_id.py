# -*- coding: utf-8 -*-
import os
from slackclient import SlackClient

BOT_NAME = 'choboi'
SLACK_TOKEN = os.environ.get('SLACK_CHOBOI_API_TOKEN')

slack_client = SlackClient(SLACK_TOKEN)

if __name__ == '__main__':
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("BOT ID for {} is {}".format(
                    user['name'], user.get('id'))
                )
            else:
                print('sup')
    else:
        print(api_call)
