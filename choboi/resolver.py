# -*- coding: utf-8 -*-
import re
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

Command = namedtuple('Command', ['args', 'action'])

global_commands = {}
mention_commands = {}
_default_command = None


def static_response(output):
    def inner(*args, **kwargs):
        return output
    return inner


def text_response(pattern, output, mention=False):
    def inner(*args, **kwargs):
        return output
    return register_command(pattern, mention)(inner)


def register_command(pattern, mention=False):
    logger.info("registering: %s", pattern)
    def wrapper(func):
        if mention:
            mention_commands[re.compile(pattern)] = func
        else:
            global_commands[re.compile(pattern)] = func
        return func
    return wrapper


def default_command():
    logger.info("registering default command")
    if _default_command is not None:
        logger.error("over writing current default command")
    def wrapper(func):
        global _default_command # pylint: disable=global-statement
        _default_command = func
        return func
    return wrapper


def resolve(text, at=None, handle_default=True):
    """
    Given a text input from user and a dictionary containing of command: action,
    returns a Command object for the bot to perform.
    """
    # Empty string, just return
    if not text:
        return None

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
        if handle_default:
            logger.info(_default_command)
            return Command(action=_default_command, args=[])
        return None

    return output


def _search(text, commands):
    for pattern, action in commands.items():
        match = pattern.match(text.lower())
        if match:
            args = match.groups() or []
            return Command(action=action, args=args)
    return None
