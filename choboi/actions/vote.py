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

vote_storage = storage.JSONStorage("votes.json")
giver_storage = storage.JSONStorage("givers.json")
taker_storage = storage.JSONStorage("takers.json")

@register_command('\<\@(?P<uid>.+)\>\s*\+\+')
def vote_up(*args, **kwargs):
    votes = vote_storage.get()
    uid = args[0].lower()
    user = kwargs.get('user', '').lower()
    target = get_user(uid)
    name = target.get('name')
    display_name = target['profile']['display_name']

    if uid == user or user == "b3gknlxl7":
        if uid in votes and uid != "u3942s8pn":
            votes[uid]["votes"] = 0
        vote_storage.save(votes)
        return "you can't game the system bro"

    points = votes.get(uid, {}).get('votes') or 0
    points += 1
    votes[uid] = {
        'votes': points,
        'name': name,
        'display_name': display_name
    }
    vote_storage.save(votes)
    get_giver(user)
    return "<@{}> one bluecoin for you homie".format(votes[uid]["name"])


def get_giver(uid):
    user_info = get_user(uid)
    name = user_info.get('name')
    display_name = user_info['profile']['display_name']
    save_giver(name, display_name, uid)


def save_giver(name, display_name, uid):
    votes_given = giver_storage.get();

    points_given = votes_given.get(uid, {}).get('votes_given') or 0
    points_given += 1
    votes_given[uid] = {
        'votes_given': points_given,
        'name': name,
        'display_name': display_name
    }
    giver_storage.save(votes_given)


@register_command('\<\@(?P<uid>.+)\>\s*\-\-')
def vote_down(*args, **kwargs):
    votes = vote_storage.get()
    uid = args[0].lower()
    if uid not in votes:
        votes[uid] = {"name": name, "votes": -1}
    else:
        votes[uid]["votes"] -= 1
    vote_storage.save(votes)

    return "<@{}> lost a bluecoin yo".format(votes[uid]["name"])


def get_taker(uid):
    user_info = get_user(uid)
    name = user_info.get('name')
    display_name = user_info['profile']['display_name']
    save_taker(name, display_name, uid)


def save_taker(name, display_name, uid):
    votes_taken = taker_storage.get();

    points_taken = votes_taken.get(uid, {}).get('votes_taken') or 0
    points_taken += 1
    votes_taken[uid] = {
        'votes_taken': points_taken,
        'name': name,
        'display_name': display_name
    }
    taker_storage.save(votes_taken)


@register_command('^print bluecoin', mention=False)
def print_votes(*args, **kwargs):
    votes = vote_storage.get()
    sortedVotes = sorted(votes.items(), key=lambda x:x[1]["votes"], reverse=True)
    return "\n".join(["{}: {}".format(v["display_name"], v["votes"]) for _, v in sortedVotes])


@register_command('whos being generous', mention=False)
def print_givers(*args, **kwargs):
    votes_given = giver_storage.get();
    sorted_giver_votes = sorted(votes_given.items(), key=lambda x:x[1]["votes_given"], reverse=True)
    return "\n".join(["{}: {}".format(v["display_name"], v["votes_given"]) for _, v in sorted_giver_votes])


@register_command('whos being mean', mention=False)
def print_takers(*args, **kwargs):
    votes_taken = taker_storage.get();
    sorted_taker_votes = sorted(votes_taken.items(), key=lambda x:x[1]["votes_taken"], reverse=True)
    return "\n".join(["{}: {}".format(v["display_name"], v["votes_taken"]) for _, v in sorted_taker_votes])


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
