# -*- coding: utf-8 -*-
"""
random stuff
"""
from ..resolver import register_command


@register_command('say (.+)', mention=True)
def say(*args, **kwargs):
    return "fucka you whale. {}".format(args[0])


@register_command('^soo*$')
def sososo(*args, **kwargs):
    return "so" * random.randin(3, 16)
