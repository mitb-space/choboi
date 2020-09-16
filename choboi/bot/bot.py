import logging
import threading
import queue

import sqlalchemy
from slackclient import SlackClient

from choboi.bot import config
from choboi.bot.listener import SlackListener
from choboi.bot.responder import SlackResponder
from choboi.bot.handler import Handler
from choboi.bot.recorder.recorder import RecorderMiddleare
from choboi.bot.scheduler import Scheduler

logger = logging.getLogger(__name__)


class Bot:
    num_handlers = 1

    def __init__(self):
        self.bot_id = config.BOT_ID

        self.middlewares = []

        self.client = None

        # database
        self.db = None

        # thread settings
        self.delay = config.THREAD_DELAY
        self.input_queue = queue.Queue()
        self.output_queue = queue.Queue()
        self.threads = []

    def __connect_slack(self):
        # configure listener
        client = SlackClient(config.SLACK_TOKEN)

        if not client.rtm_connect(auto_reconnect=True):
            logger.exception("unable to connect to slack RTM service")
            raise Exception("Unable to connect to slack RTM service")
        logger.info("connected to slack")

        self.client = client

    def __connect_db(self):
        if config.DATABASE_URL:
            self.db = sqlalchemy.create_engine(config.DATABASE_URL)

    def __register_middlewares(self):
        self.middlewares = [
            RecorderMiddleare(self.db),
        ]

    def run(self):
        self.__connect_db()
        self.__connect_slack()
        self.__register_middlewares()

        listener = SlackListener(self.input_queue, self.delay, self.client, self.bot_id)
        self.threads.append(threading.Thread(target=listener.run))

        responder = SlackResponder(self.output_queue, self.delay, self.client, self.bot_id)
        self.threads.append(threading.Thread(target=responder.run))

        scheduler = Scheduler(self.output_queue, self.delay, self.client, self.db)
        self.threads.append(threading.Thread(target=scheduler.run))

        handler = Handler(self.input_queue, self.output_queue, self.bot_id, self.delay, self.db, self.middlewares)
        self.threads.append(threading.Thread(target=handler.run))

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
