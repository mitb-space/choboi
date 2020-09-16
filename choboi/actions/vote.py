# -*- coding: utf-8 -*-
"""
handles user++ user-- scores
"""
import logging

import requests

from choboi.resolver import register_command
from choboi.bot.config import SLACK_TOKEN
from choboi.votes.models import Vote
from choboi.db.transaction import begin_tx

logger = logging.getLogger(__name__)

banned = [
    'b3gknlxl7',
    'uslackbot',
]

users = {}


@register_command(r'\<\@(?P<uid>.+)\>\s*\+\+')
@begin_tx
def vote_up(*args, **kwargs):
    to = args[0].lower()
    actor = kwargs.get('user', '').lower()

    tx = kwargs.get('tx')

    if to == actor or actor in banned:
        vote = Vote.down(actor, to)
        tx.add(vote)
        return "you can't game the system bro"

    vote = Vote.up(actor, to)
    tx.add(vote)
    return "one bluecoin for my homie"


@register_command(r'\<\@(?P<uid>.+)\>\s*\-\-')
@begin_tx
def vote_down(*args, **kwargs):
    to = args[0].lower()
    actor = kwargs.get('user', '').lower()
    tx = kwargs.get('tx')

    vote = Vote.down(actor, to)
    tx.add(vote)

    return "oof lost a bluecoin yo"


@register_command('^print bluecoin', mention=False)
@begin_tx
def print_votes(*args, **kwargs):
    tx = kwargs.get('tx')

    output = 'rich homies:\n'
    result = Vote.aggregate_votes(tx)
    for rec_id, votes in result:
        name = display_name(rec_id)
        output += '{}: {}\n'.format(name, votes)
    return output


def display_name(uid):
    if uid not in users:
        u = get_user(uid)
        if u:
            users[uid] = u
    u = users.get(uid)
    if u:
        return u.get('profile', {}).get('display_name')
    return 'anonymous homie'


@register_command("who'?s being generous", mention=False)
def print_givers(*args, **kwargs):
    return "sorry dawg, we need to rewrite this"


@register_command("who'?s being mean", mention=False)
def print_takers(*args, **kwargs):
    return "sorry dawg, we need to rewrite this"


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
    logger.info("fetched user info %s", r.json())
    return r.json().get("user")
