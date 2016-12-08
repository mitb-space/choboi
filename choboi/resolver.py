# -*- coding: utf-8 -*-
import re
from collections import namedtuple

from .actions import *  # noqa


Command = namedtuple('Command', ['args', 'kwargs', 'action'])

# these should come from the bot
root_global_commands = {
    re.compile('^take me.*'): take_me_to_da_movies,
    re.compile('.*her+o.*'): herro,
    re.compile('^is (?P<name>\w+) a cuck'): is_a_cuck,
    re.compile('^who.+a cuck'): who_is_a_cuck,
    re.compile('^guys\S*$'): homies_assemble,
    re.compile('.*<!everyone>.*'): homies_assemble,
    re.compile('.*dank meme.*'): dank_meme,
    re.compile('.*trebuchet.*'): trebuchet,
    re.compile('^k{3,}'): racist
}
root_at_commands = {
    re.compile('^help$'): print_help,
    re.compile('.*fucka? you.*'): fucka_you,
    re.compile('.*hey look.*'): oh_shit_waddup,
    re.compile('say (.+)'): say
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
        text = text.replace(at, '').strip()

    # Search  commands
    for commands in (global_commands, at_commands,):
        output = _search(text, commands)
        if output:
            break

    # no output and no @
    if not output and at_in_text:
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
