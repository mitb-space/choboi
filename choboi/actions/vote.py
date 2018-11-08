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

# hard coding current points since there are no storage :(
votes = {
    'u9yhuck2b': {
        "name": "acferrel2",
        "votes": 20,
    },
    'u6fcp87hr': {
        "name": "recursiveowl",
        "votes": 54,
    },
    'u39m0htja': {
        "name": "pogopunkxiii",
        "votes": 49,
    },
    'u389xuht2': {
        "name": "grehg",
        "votes": 216,
    },
    'u5p2rm132': {
        "name": "mike",
        "votes": 40,
    },
    'u3942s8pn': {
        "name": "dave",
        "votes": 300,
    },
    'u38uw3edr': {
        "name": "who_dat",
        "votes": 4,
    },
    'u7rq3bce5': {
        "name": "molly.l.perham",
        "votes": 1,
    },
}


@register_command('\<\@(?P<uid>.+)\>\s*\+\+')
def vote_up(*args, **kwargs):
    uid = args[0].lower()
    if uid == kwargs.get('user') or uid == "B3GKNLXL7":
        if uid in votes:
            votes[uid]["votes"] = 0
        return "you can't game the system bro"
    if uid not in votes:
        name = get_username(uid)
        votes[uid] = {"name": name, "votes": 1}
    else:
        votes[uid]["votes"] += 1
    votes['U3942S8PN']["votes"] += 1  # shhh
    print(votes)
    return "<@{}> gained a point yo".format(votes[uid]["name"])


@register_command('\<\@(?P<uid>.+)\>\s*\-\-')
def vote_down(*args, **kwargs):
    uid = args[0].lower()
    if uid not in votes:
        name = get_username(uid)
        votes[uid] = {"name": name, "votes": -1}
    else:
        votes[uid]["votes"] -= 1
    return "<@{}> lost a point yo".format(votes[uid]["name"])


@register_command('^print votes', mention=True)
def print_votes(*args, **kwargs):
    sortedVotes = sorted(votes.items(), key=lambda x:x[1]["votes"], reverse=True)
    return "\n".join(["{}: {}".format(v["name"], v["votes"]) for _, v in sortedVotes])


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
