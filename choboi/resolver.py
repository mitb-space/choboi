# -*- coding: utf-8 -*-
import re
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

Command = namedtuple('Command', ['args', 'action'])

global_commands = {}
mention_commands = {}


def text_response(pattern, output, mention=False):
    def inner(*args, **kwargs):
        return output
    return register_command(pattern, mention)(inner)


def register_command(pattern, mention=False):
    logger.info("registering: {}".format(pattern))
    def wrapper(func):
        if mention:
            mention_commands[re.compile(pattern)] = func
        else:
            global_commands[re.compile(pattern)] = func
        return func
    return wrapper


# TODO: default response should come from the bot
default = text_response("supboi", "gtfo bro, i didn't hear a word")

DEFAULT_COMMAND = Command(action=default, args=[])


def resolve(text, at=None):
    """
    Given a text input from user and a dictionary containing of command: action,
    returns a Command object for the bot to perform.
    """
    # Empty string, just return
    if not text:
        return

    at = at.lower()
    at_in_text = False
    if at and at in text:
        at_in_text = True
        text = text.replace(at, '').strip()

    # We only care about at_commands if at_in_text is true
    search_commands = [global_commands,]
    if at_in_text:
        search_commands.append(mention_commands)

    # Search  commands
    for commands in search_commands:
        output = _search(text, commands)
        if output:
            break

    # no output and @
    if not output and at_in_text:
        return DEFAULT_COMMAND

    return output


def _search(text, commands):
    for pattern, action in commands.items():
        match = pattern.match(text)
        if match:
            args = match.groups() or []
            return Command(action=action, args=args)
