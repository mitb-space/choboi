# -*- coding: utf-8 -*-
import random
from ..resolver import register_command

cucks = {}

YES = "yea boiii"
NO = "nah bby"


@register_command('^is (?P<name>\w+) a cuck')
def is_a_cuck(*args, **kwargs):
    name = args[0].lower()
    if name not in cucks:
        cucks[name] = YES if random.randint(0, 1) else NO
    return cucks[name]


@register_command('^who.+a cuck')
def who_is_a_cuck(*args, **kwargs):
    return ", ".join(
        [name for name, is_a_cuck in cucks.items() if is_a_cuck == YES]
    )
