import logging
import time

from .event import OutputEvent
from ..resolver import resolve

from .. import actions # pylint: disable=unused-import

logger = logging.getLogger(__name__)


class Handler:
    """
    Handler reads input events from the input queue and processes them.  If
    there are any outputs, it appends the OutputEvent onto the output queue.
    """

    def __init__(self, input_queue, output_queue, bot_id, delay, db):
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.bot_id = bot_id
        self.delay = delay
        self.alive = True
        self.db = db

    def run(self):
        while self.alive:
            try:
                time.sleep(self.delay)
                if self.input_queue.empty():
                    continue
                input_event = self.input_queue.get()
                if not input_event:
                    continue
                output_event = self.__resolve(input_event)
                if output_event:
                    logger.info("resolved message: %s", output_event)
                    self.output_queue.put_nowait(output_event)
            except Exception as ex:
                logger.error("error: %s", ex)

    def __resolve(self, input_event):
        """
        resolves an input event into an output event
        """
        logger.info(input_event)
        cmd = resolve(input_event.message, at=self.bot_id, handle_default=True)
        logger.info("action: %s", cmd)
        if not cmd:
            return None

        message = cmd.action(
            *cmd.args,
            user=input_event.user_id,
            message=input_event.message,
            channel=input_event.channel,
            conn=self.db,
        )
        return OutputEvent(
            channel=input_event.channel,
            message=message)
