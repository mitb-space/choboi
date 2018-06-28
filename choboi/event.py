# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

events = []

Event = namedtuple('Event', ['name', 'frequency', 'channel', 'action'])


def register_event(name, frequency=60, channel=None):
    """
    registers a reoccuring event
    """
    logger.info(f'registering event: {name}')
    def wrapper(func):
        events.append(Event(name, frequency, channel, func))
        return func
    return wrapper
