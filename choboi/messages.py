# -*- coding: utf-8 -*-


def get_message_text(messages):
    response = []
    for m in messages:
        if m.get('type') == 'message':
            text = m.get('text', '')
            response.append(text)
    return response