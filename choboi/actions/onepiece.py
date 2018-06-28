# -*- coding: utf-8 -*-
import requests
from collections import namedtuple
from ..event import register_event

Chapter = namedtuple('Chapter', ['chapter', 'link'])

chapters = []

@register_event(name='one-piece-chapter', frequency=600, channel='#anime')
def new_chapter():
    posts = get_posts()
    if len(chapters) == 0:
        last_chapter = 0
    else:
        last_chapter = chapters[-1].chapter
    for p in posts:
        data = p['data']
        if data['link_flair_text'] == 'Current Chapter':
            title = data['title']
            nums = [int(s) for s in title.split() if s.isdigit()]
            if len(nums) > 0:
                chapter = nums[0]
                if last_chapter != chapter:
                    last_chapter = chapter
                    link = data['url']
                    chapters.append(Chapter(last_chapter, link))
                    return f'<!channel> dank chapter {last_chapter} is up: {link}'


def get_posts():
    r = requests.get(
        'https://www.reddit.com/r/OnePiece/.json',
        headers = {'User-agent': 'choboi'}
    ).json()
    return r['data']['children']
