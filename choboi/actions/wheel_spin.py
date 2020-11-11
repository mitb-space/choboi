# -*- coding: utf-8 -*-
import logging
import random

import schedule

from choboi.bot.scheduler import add_schedule
from choboi.db.transaction import begin_tx
from choboi.votes.models import Vote

img_url = 'https://imgur.com/frdKT6E'

logger = logging.getLogger(__name__)


# 9am est
@add_schedule(name='wheel-spin', schedule=schedule.every().day.at('14:00'), channel='#shit-posts')
@begin_tx
def wheel_spin(*args, **kwargs):
    tx = kwargs.get('tx')

    # anyone with bluecoin is eligible
    result = Vote.aggregate_votes(tx).fetchall()
    winner = random.choice(result)
    return f'<@{winner[0].upper()}> /roll 1d6 (yellow = 1, clockwise)\n{img_url}'
