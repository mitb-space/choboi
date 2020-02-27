from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Vote(Base):
    __tablename__ = 'votes'
    id = Column(Integer, primary_key=True)
    giver_id = Column(String)
    recipient_id = Column(String)
    created_at = Column(DateTime, default=func.now())
    amount = Column(Integer)

    @classmethod
    def up(cls, giver_id, recipient_id):
        return Vote(
            giver_id=giver_id,
            recipient_id=recipient_id,
            amount=1)

    @classmethod
    def down(cls, giver_id, recipient_id):
        return Vote(
            giver_id=giver_id,
            recipient_id=recipient_id,
            amount=-1)
