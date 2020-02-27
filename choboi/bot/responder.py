import logging
import time

logger = logging.getLogger(__name__)


class SlackResponder:
    """
    SlackResponder listens for a new output event from the output queue.  It
    will then send the output to slack.
    """

    def __init__(self, queue, delay, slack_client, bot_id):
        self.queue = queue
        self.alive = True
        self.delay = delay
        self.slack_client = slack_client
        self.bot_id = bot_id

    def run(self):
        """
        output message to slack
        """
        while self.alive:
            try:
                time.sleep(self.delay)
                if self.queue.empty():
                    continue
                output_event = self.queue.get()
                if not output_event:
                    continue
                self.__respond(output_event)
                logger.info("responded to slack")
            except Exception as ex:
                logger.error("error: %s", ex)

    def __respond(self, output_event):
        self.slack_client.api_call(
            "chat.postMessage",
            channel=output_event.channel,
            text=output_event.message,
            as_user=True,
        )
