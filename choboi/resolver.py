# -*- coding: utf-8 -*-
import re
from collections import namedtuple

from .actions import (
    print_help, herro, is_a_cuck, who_is_a_cuck
)


Command = namedtuple('Command', ['args', 'kwargs', 'action'])

root_commands = {
    re.compile('^help$'): print_help,
    re.compile('^herro$'): herro,
    re.compile('^is (?P<name>\w+) a cuck'): is_a_cuck,
    re.compile('^who.+a cuck'): who_is_a_cuck,
}

HELP_COMMAND = Command(action=print_help, args=[], kwargs={})


def resolve(text, commands=root_commands):
    """
    Given a text input from user and a dictionary containing of command: action,
    returns a Command object for the bot to perform.
    """
    # strip special characters and make it lower case.
    text = text.strip()

    # Empty string, so print the help command
    if not text:
        return HELP_COMMAND

    # Find the command
    for pattern, action in commands.items():
        match = pattern.match(text)
        if match:
            # TODO get group name
            args = match.groups() or []
            kwargs = {}
            return Command(action=action, args=args, kwargs=kwargs)

    # If we're here, we didn't find the command
    return None
