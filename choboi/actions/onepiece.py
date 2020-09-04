# -*- coding: utf-8 -*-
import requests
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text

from choboi.bot.scheduler import schedule
from choboi.db.transaction import begin_tx

Base = declarative_base()


class Chapter(Base):
    __tablename__ = 'one_piece_chapters'
    chapter = Column(Integer, primary_key=True)
    link = Column(String)

    @classmethod
    def get_latest_chapter(cls, conn):
        stmt = text(
            'SELECT chapter, link '
            'FROM one_piece_chapters '
            'ORDER BY chapter DESC LIMIT 1 '
        )
        stmt.columns(cls.chapter, cls.link)
        result = conn.execute(stmt).fetchone()
        if result is not None:
            return result[0]
        return None


@schedule(name='one-piece-chapter', frequency=600, channel='#anime')
@begin_tx
def new_chapter(*args, **kwargs):
    tx = kwargs.get('tx')
    last_chapter = Chapter.get_latest_chapter(tx)
    posts = get_posts()
    for p in posts:
        data = p['data']
        if data['link_flair_text'] == 'Current Chapter':
            title = data['title']
            nums = [int(s) for s in title.split() if s.isdigit()]
            if nums:
                chapter = nums[0]
                if last_chapter != chapter:
                    last_chapter = chapter
                    link = data['url']
                    tx.add(
                        Chapter(
                            chapter=chapter,
                            link=link,
                        ))
                    return f':wave: New One Piece #{last_chapter} is up: {link}'
    return None


def get_posts():
    r = requests.get(
        'https://www.reddit.com/r/OnePiece/.json',
        headers={'User-agent': 'choboi'}
    ).json()
    return r['data']['children']
