from sqlalchemy import Column, DateTime, String, Integer, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

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

    @classmethod
    def aggregate_votes(cls, conn):
        """
        returns a list of (recipient_id, vote_count)
        """
        stmt = text(
            'SELECT recipient_id, SUM(amount) AS amount '
            'FROM votes '
            'GROUP BY recipient_id'
        )
        return conn.execute(stmt)
