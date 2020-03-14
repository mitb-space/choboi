from sqlalchemy.orm import Session

from .models import Message


class RecorderMiddleare:

    def __init__(self, conn):
        self.conn = conn

    def process_input(self, input_event):
        m = Message(
            user_id=input_event.user_id,
            channel_id=input_event.channel,
            message=input_event.message,
        )
        session = Session(bind=self.conn)
        session.add(m)
        session.commit()
