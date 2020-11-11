# -*- coding: utf-8 -*-
import logging
import time
from collections import namedtuple
import schedule as schd

logger = logging.getLogger(__name__)

events = []

Event = namedtuple('Event', ['name', 'schedule', 'channel', 'action'])

def add_schedule(name, schedule, channel):
    logger.info('registering event: %s', name)
    def wrapper(func):
        events.append(Event(name, schedule, channel, func))
        return func
    return wrapper


class Scheduler:
    def __init__(self, queue, delay, slack_client, db):
        self.queue = queue
        self.delay = delay
        self.alive = True
        self.client = slack_client
        self.db = db

    def run(self):
        for e in events:
            e.schedule.do(self.__run_scheduled_event(e))

        while self.alive:
            time.sleep(self.delay)
            schd.run_pending()

    def __run_scheduled_event(self, event: Event):
        def func():
            logger.info('running scheduled event %s', event)
            try:
                response = event.action(conn=self.db)
                if response:
                    logging.info('Responding %s')
                    # TODO: output queue
                    self.client.api_call(
                        "chat.postMessage",
                        channel=event.channel,
                        text=response,
                        as_user=True
                    )
            except Exception as ex:
                logger.error('failed to process scheduled event %s', ex)
        return func
