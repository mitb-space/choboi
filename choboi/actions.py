# -*- coding: utf-8 -*-
import random

cucks = {}

HELP_TEXT = """
Here are phrases I understand:

    herro
    is <name> a cuck?
    who is a cuck?
"""

default = text_response("Sorry, I don't understand")
print_help = text_response(HELP_TEXT)
take_me_to_da_movies = text_response(
    "i'll take you to da mooovies {}".format("https://youtu.be/GzaUddim4X4")
)
herro = text_response("parese")


def is_a_cuck(*args, **kwargs):
    name = args[0].lower()
    if name not in cucks:
        cucks[name] = 'Yes' if random.randint(0, 1) else 'No'
    return cucks[name]


def who_is_a_cuck(*args, **kwargs):
    return ", ".join(
        [name for name, is_a_cuck in cucks.items() if is_a_cuck == 'Yes']
    )

def simple_text_command(output):
    def inner(*args, **kwargs):
        return output
    return inner
