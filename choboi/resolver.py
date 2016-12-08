# -*- coding: utf-8 -*-
import re
from collections import namedtuple

from .actions import (
    print_help, herro, is_a_cuck, who_is_a_cuck, take_me_to_da_movies,
    default
)


Command = namedtuple('Command', ['args', 'kwargs', 'action'])

root_global_commands = {
    re.compile('^take me.*'): take_me_to_da_movies,
    re.compile('^herro$'): herro,
    re.compile('^is (?P<name>\w+) a cuck'): is_a_cuck,
    re.compile('^who.+a cuck'): who_is_a_cuck,
}
root_at_commands = {
    re.compile('^help$'): print_help,
}

HELP_COMMAND = Command(action=print_help, args=[], kwargs={})
DEFAULT_COMMAND = Command(action=default, args=[], kwargs={})


def resolve(
    text,
    global_commands=root_global_commands,
    at_commands=root_at_commands,
    at=''
):
    """
    Given a text input from user and a dictionary containing of command: action,
    returns a Command object for the bot to perform.
    """
    # Empty string, so print the help command
    if not text:
        return HELP_COMMAND

    at = at.lower()
    at_in_text = False
    if at and at in text:
        at_in_text = True
        text = text.split(at)[1].strip()

    # Search global commands
    output = _search(text, global_commands)

    # search @ commands
    if at_in_text:
        output = _search(text, at_commands)
        if not output:
            return DEFAULT_COMMAND

    return output


def _search(text, commands):
    for pattern, action in commands.items():
        match = pattern.match(text)
        if match:
            # TODO get group name
            args = match.groups() or []
            kwargs = {}
            return Command(action=action, args=args, kwargs=kwargs)
