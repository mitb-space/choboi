import logging
import threading
import queue

import sqlalchemy
from slackclient import SlackClient

from . import config
from .listener import SlackListener
from .responder import SlackResponder
from .handler import Handler

logger = logging.getLogger(__name__)


class Bot:
    num_slack_listeners = 1
    num_slack_responders = 1
    num_handlers = 1

    def __init__(self):
        self.bot_id = config.BOT_ID

        # database
        self.db = None

        # thread settings
        self.delay = config.THREAD_DELAY
        self.input_queue = queue.LifoQueue()
        self.output_queue = queue.LifoQueue()
        self.threads = []

    def __connect_slack(self):
        # configure listener
        client = SlackClient(config.SLACK_TOKEN)

        if not client.rtm_connect(auto_reconnect=True):
            logger.exception("unable to connect to slack RTM service")
            raise Exception("Unable to connect to slack RTM service")
        logger.info("connected to slack")

        for _ in range(self.num_slack_listeners):
            l = SlackListener(self.input_queue, self.delay, client, self.bot_id)
            self.threads.append(threading.Thread(target=l.run))
        for _ in range(self.num_slack_responders):
            r = SlackResponder(self.output_queue, self.delay, client, self.bot_id)
            self.threads.append(threading.Thread(target=r.run))

    def __connect_db(self):
        if config.DATABASE_URL:
            engine = sqlalchemy.create_engine(config.DATABASE_URL)
            self.db = engine.connect()

    def run(self):
        # configure
        self.__connect_slack()
        self.__connect_db()
        for _ in range(self.num_handlers):
            h = Handler(self.input_queue, self.output_queue, self.bot_id, self.delay)
            self.threads.append(threading.Thread(target=h.run))

        # go
        for t in self.threads:
            try:
                t.start()
            except Exception as ex:
                logging.error("failed to start thread: %s", ex)

        # wait
        for t in self.threads:
            try:
                if t.is_alive():
                    t.join()
            except (KeyboardInterrupt, SystemExit):
                logging.info('Received keyboard interrupt, quitting threads')
                return
