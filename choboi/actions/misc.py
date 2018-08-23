# -*- coding: utf-8 -*-
"""
random stuff
"""
import random
from ..resolver import register_command


@register_command('say (.+)', mention=True)
def say(*args, **kwargs):
    return "fucka you whale. {}".format(args[0])


@register_command('^soo*$')
def sososo(*args, **kwargs):
    return "so" * random.randint(3, 16)

@register_command('.*crunch the .+')
def crunch_numbies(*args, **kwargs):
    operations = [
        'added',
        'took the integral of',
        'calculated the fourier transform of',
        'analyzed the conditional and joint distribution of',
        'took the Riemann hypothesis of',
        'first I proved P vs. NP and now it looks like',
        'made my way down town to',
    ]
    targets = [
        'your mom',
        'moms spaghet',
        'my homies',
        'dank memes',
        'bluebrush',
        'tasty treats',
    ]
    repeating = '3' * random.randint(2, 10)
    operation = operations[random.randint(0, len(operations)-1)]
    target = targets[random.randint(0, len(targets)-1)]
    return f'I {operation} {target} and the number comes out to .{repeating}.\nrepeating of course'
