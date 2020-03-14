import logging
import time

from .event import (
    MessageEvent,
    ErrorEvent
)


logger = logging.getLogger(__name__)


class SlackListener:
    """
    Listener listens for new events from slack.  It converts known slack event
    types into internal Event object and puts it on the queue.
    """

    def __init__(self, queue, delay, slack_client, bot_id):
        self.queue = queue
        self.alive = True
        self.delay = delay
        self.slack_client = slack_client
        self.bot_id = bot_id

    def run(self):
        """
        Append slack output to the queue
        """
        while self.alive:
            time.sleep(self.delay)
            try:
                slack_inputs = self.slack_client.rtm_read()
                if slack_inputs:
                    events = self.__process_input(slack_inputs)
                    for event in events:
                        self.queue.put_nowait(event)
            except Exception as ex:
                logger.error("listener exception: %s", ex)

    def __process_input(self, slack_inputs):
        events = []
        for slack_input in slack_inputs:
            if slack_input:
                event = self.__handle_slack_input(slack_input)
                if event:
                    logging.info("appending: %s", event)
                    events.append(event)
        return events

    def __handle_slack_input(self, slack_input):
        """
        __handle_slack_input converts the given input from slack to Event class
        """
        if slack_input.get('type') == 'message':
            if slack_input.get('user') == self.bot_id:
                return None
            text = slack_input.get('text', '').strip()
            if text:
                return MessageEvent(
                    type='message',
                    user_id=slack_input.get('user'),
                    message=text,
                    channel=slack_input.get('channel'),
                )
        elif slack_input.get('type') == 'error':
            return ErrorEvent(
                type='error',
                user_id=slack_input.get('user'),
                error=slack_input.get('error'),
                code=slack_input.get('code'),
                msg=slack_input.get('msg'),
            )
        else:
            logger.info("unhandled event: %s", slack_input)
        return None
