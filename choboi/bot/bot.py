import logging
import threading
import queue

import sqlalchemy
from slackclient import SlackClient

from . import config
from .listener import SlackListener
from .responder import SlackResponder
from .handler import Handler
from .recorder.recorder import RecorderMiddleare

logger = logging.getLogger(__name__)


class Bot:
    num_handlers = 1

    def __init__(self):
        self.bot_id = config.BOT_ID

        self.middlewares = []

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

        listener = SlackListener(self.input_queue, self.delay, client, self.bot_id)
        self.threads.append(threading.Thread(target=listener.run))

        responder = SlackResponder(self.output_queue, self.delay, client, self.bot_id)
        self.threads.append(threading.Thread(target=responder.run))

    def __connect_db(self):
        if config.DATABASE_URL:
            engine = sqlalchemy.create_engine(config.DATABASE_URL)
            self.db = engine.connect()

    def __register_middlewares(self):
        self.middlewares = [
            RecorderMiddleare(self.db),
        ]

    def run(self):
        self.__connect_slack()
        self.__connect_db()
        self.__register_middlewares()
        for _ in range(self.num_handlers):
            h = Handler(self.input_queue, self.output_queue, self.bot_id, self.delay, self.db, self.middlewares)
            self.threads.append(threading.Thread(target=h.run))

        for t in self.threads:
            try:
                t.start()
            except Exception as ex:
                logging.error("failed to start thread: %s", ex)

        for t in self.threads:
            try:
                if t.is_alive():
                    t.join()
            except (KeyboardInterrupt, SystemExit):
                logging.info('Received keyboard interrupt, quitting threads')
                return
