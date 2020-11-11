# -*- coding: utf-8 -*-
import logging
import random

import schedule

from choboi.bot.scheduler import add_schedule
from choboi.db.transaction import begin_tx
from choboi.votes.models import Vote

img_url = 'https://imgur.com/frdKT6E'

logger = logging.getLogger(__name__)


@add_schedule(name='wheel-spin', schedule=schedule.every().day.at('09:00'), channel='#dev-bot')
@begin_tx
def wheel_spin(*args, **kwargs):
    logger.info('starting wheel spin')
    tx = kwargs.get('tx')

    # anyone with bluecoin is eligible
    result = Vote.aggregate_votes(tx)

    # testing
    allow = ['u3942s8pn']
    result = filter(lambda x: x[0] in allow, result)

    winner = random.choice(result)
    return f'<@{winner}> {img_url}'
