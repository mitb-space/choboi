# -*- coding: utf-8 -*-
import requests

from ..event import register_event

@register_event(name='haiku', at='7:00', channel='#shit-posts')
def new_chapter():
    posts = get_posts()
    highest = 0
    link = ''
    for p in posts:
        data = p['data']
        score = data['score']
        if score > highest:
            highest = score
            link = data['url']
    if highest:
        return f'dank {link}'
    return None


def get_posts():
    r = requests.get(
        'https://www.reddit.com/r/youtubehaiku/.json',
        headers={'User-agent': 'choboi'}
    ).json()
    return r['data']['children']
