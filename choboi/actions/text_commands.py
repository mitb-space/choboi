# -*- coding: utf-8 -*-
"""
This file contains raw text -> text interactions
"""
from ..resolver import text_response

herro = text_response(
    '.*her+o.*',
    "parese"
)

up_arrow = text_response(
    r'\^',
    '^'
)

this_response = text_response(
    '.*:this:.*',
    ':this:'
)

oh_shit_waddup = text_response(
    '.*hey look.*',
    "oh shit waddaup {}".format("http://media3.giphy.com/media/UHKL9BtyM4WrK/giphy.gif"),
    mention=True
)

dank = text_response(
    "[dD]ank",
    "k."
)

math_checks_out = text_response(
    r".+\%",
    "math checks out"
)

be_nice = text_response(
    r"\(╯°□°）╯︵ ┻━┻",
    "┬─┬ ノ( ゜-゜ノ)"
)
