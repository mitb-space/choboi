from sqlalchemy import Column, DateTime, String, Integer, Text, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    channel_id = Column(String)
    message = Column(Text)
    created_at = Column(DateTime, default=func.now())
