# -*- coding: utf-8 -*-
"""
handles user++ uesr-- scores
"""
import logging
from collections import namedtuple

import requests

from ..resolver import register_command
from ..config import SLACK_TOKEN

logger = logging.getLogger(__name__)
votes = {}


@register_command('\<\@(?P<uid>.+)\>\+\+')
def vote_up(*args, **kwargs):
    print("sup")
    uid = args[0].lower()
    if uid not in votes:
        name = get_username(uid)
        votes[uid] = {"name": name, "votes": 1}
    else:
        votes[uid]["votes"] += 1
    return "<@{}> gained a point yo".format(votes[uid]["name"])


@register_command('^print votes', mention=True)
def print_votes(*args, **kwargs):
    return "\n".join(["{}: {}".format(v["name"], v["votes"]) for _, v in votes.items()])


def get_username(user_id):
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    payload = {
        "token": SLACK_TOKEN,
        "user": user_id.upper(),
    }
    r = requests.post(
        'https://slack.com/api/users.info',
        headers=headers,
        data=payload,
    )
    logger.info("fetched user info {}".format(r.json()))
    return r.json().get("user").get("name")
