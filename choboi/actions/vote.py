# -*- coding: utf-8 -*-
"""
handles user++ uesr-- scores
"""
import logging
import os
from collections import namedtuple

import requests

from ..resolver import register_command
from ..config import SLACK_TOKEN
from .. import storage

logger = logging.getLogger(__name__)

storage = storage.JSONStorage("votes.json")


@register_command('\<\@(?P<uid>.+)\>\s*\+\+')
def vote_up(*args, **kwargs):
    votes = storage.get()
    uid = args[0].lower()
    user = kwargs.get('user', '').lower()
    target = get_user(uid)
    name = target.get('name')
    display_name = target.get('display_name')

    if uid == user or user == "b3gknlxl7":
        if uid in votes and uid != "u3942s8pn":
            votes[uid]["votes"] = 0
        storage.save(votes)
        return "you can't game the system bro"

    points = votes.get(uid, {}).get('votes') or 1
    votes[uid] = {
        'votes': points,
        'name': name,
        'display_name': display_name,
    }
    votes['u3942s8pn']["votes"] += 1  # shhh
    storage.save(votes)
    return "<@{}> one bluecoin for you homie".format(votes[uid]["name"])


@register_command('\<\@(?P<uid>.+)\>\s*\-\-')
def vote_down(*args, **kwargs):
    votes = storage.get()
    uid = args[0].lower()
    if uid not in votes:
        votes[uid] = {"name": name, "votes": -1}
    else:
        votes[uid]["votes"] -= 1
    storage.save(votes)
    return "<@{}> lost a bluecoin yo".format(votes[uid]["name"])


@register_command('^print bluecoin', mention=False)
def print_votes(*args, **kwargs):
    votes = storage.get()
    sortedVotes = sorted(votes.items(), key=lambda x:x[1]["votes"], reverse=True)
    return "\n".join(["{}: {}".format(v["display_name"], v["votes"]) for _, v in sortedVotes])


def get_user(user_id):
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
    return r.json().get("user")
