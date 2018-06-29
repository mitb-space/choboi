# -*- coding: utf-8 -*-
import logging
from collections import namedtuple

logger = logging.getLogger(__name__)

events = []

Event = namedtuple('Event', ['name', 'at', 'frequency', 'channel', 'action'])


def register_event(name, frequency=60, at=None, channel=None):
    """
    registers a reoccuring event
    """
    logger.info(f'registering event: {name}')
    def wrapper(func):
        events.append(Event(name, at, frequency, channel, func))
        return func
    return wrapper
