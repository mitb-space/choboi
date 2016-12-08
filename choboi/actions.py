# -*- coding: utf-8 -*-
import random

cucks = {}

HELP_TEXT = """
Here are phrases I understand:

    herro
    is <name> a cuck?
    who is a cuck?
"""
YES = "yea boiii"
NO = "nah bby"


def is_a_cuck(*args, **kwargs):
    name = args[0].lower()
    if name not in cucks:
        cucks[name] = YES if random.randint(0, 1) else NO
    return cucks[name]


def who_is_a_cuck(*args, **kwargs):
    return ", ".join(
        [name for name, is_a_cuck in cucks.items() if is_a_cuck == YES]
    )


def text_response(output):
    def inner(*args, **kwargs):
        return output
    return inner


default = text_response("gtfo bro, i didn't hear a word")
print_help = text_response(HELP_TEXT)
take_me_to_da_movies = text_response(
    "i'll take you to da mooovies {}".format("https://youtu.be/GzaUddim4X4")
)
herro = text_response("parese")
homies_assemble = text_response("assemble, my homies")
dank_meme = text_response("i am the dank meme king")
fucka_you = text_response("fucka you buddy")
oh_shit_waddup = text_response("oh shit waddaup {}".format(
    "http://media3.giphy.com/media/UHKL9BtyM4WrK/giphy.gif"
))
trebuchet = text_response("""
With a trebuchet, you can lob a 90kg object about 300m away.
That's 198.416 pounds 984.252 feet. WOW!
""")
