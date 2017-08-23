# -*- coding: utf-8 -*-
"""
This file contains raw text -> text interactions
"""
from ..resolver import text_response

take_me_to_da_movies = text_response(
    '^take me.*',
    "i'll take you to da mooovies {}".format("https://youtu.be/GzaUddim4X4")
)

herro = text_response(
    '.*her+o.*',
    "parese"
)

homies_assemble = text_response(
    '.*<!everyone>.*',
    'assemble, my homies'
)


dank_meme = text_response(
    '.*dank meme.*',
    'i am the dank meme king'
)

fucka_you = text_response(
    '.*fucka? you.*',
    'fucka you buddy',
    mention=True
)

oh_shit_waddup = text_response(
    '.*hey look.*',
    "oh shit waddaup {}".format("http://media3.giphy.com/media/UHKL9BtyM4WrK/giphy.gif"),
    mention=True
)

trebuchet = text_response(
    '.*trebuchet.*',
"""
With a trebuchet, you can lob a 90kg object about 300m away.
That's 198.416 pounds 984.252 feet. WOW!
"""
)

racist = text_response(
    '^k{3,}',
    "that's racist bro"
)

hes_a_nice_guy = text_response(
    "he\'?s a nice guy.*",
    "he's a nice guy... BUT"
)
