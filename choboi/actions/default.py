# -*- coding: utf-8 -*-
from ..remote.giphy import get_random_gif_by_tag
from ..resolver import default_command


@default_command()
def default_response(*args, **kwargs):
    gif_json = get_random_gif_by_tag('wat').json()
    gif_url = gif_json['data']['image_url']
    return 'wat ' + gif_url
