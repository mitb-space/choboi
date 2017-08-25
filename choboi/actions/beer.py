# -*- coding: utf-8 -*-
import random
from ..remote.brewerydb import get_beer_by_abv
from ..resolver import register_command

beer_text = """
How about a glass of {name}?

*ABV :* {abv}
*Description :* {description}
"""

@register_command('.*recommend me a beer.*')
def recommend_beer(*args, **kwargs):
    abv = random.randint(5, 14)
    beers_json = get_beer_by_abv(abv).json()
    beers = beers_json.get('data', [])
    random_beer = beers[random.randint(0, len(beers)-1)]
    msg = beer_text.format(
        name=random_beer['name'],
        description=random_beer['description'],
        abv=random_beer['abv'],
    )
    return msg
