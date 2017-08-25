# -*- coding: utf-8 -*-
from ..remote.itsthisforthat import get_random_app_idea
from ..resolver import register_command


@register_command('.*app idea.*')
def suggest_app_idea(*args, **kwargs):
    app_idea_json = get_random_app_idea().json()
    return 'yo boi, make ' + app_idea_json['this'] + ' for ' + app_idea_json['that']
