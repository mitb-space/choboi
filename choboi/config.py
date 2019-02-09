import os
from logging.config import dictConfig

PATH = os.path.dirname(os.path.realpath(__file__))

BOT_ID = os.environ.get('SLACK_BOT_ID', 'U3BMAJT2A')
SLACK_TOKEN = os.environ.get('SLACK_CHOBOI_API_TOKEN')
DEFAULT_CHANNEL = os.environ.get('SLACK_DEFAUL_CHANNEL', '#general')

MARKOV_ENABLED = os.environ.get('SLACK_CHOBOI_MARKOV_ENABLED', True)
if MARKOV_ENABLED in ("False", "false", 0):
    MARKOV_ENABLED = False

MARKOV_TRAIN_FREQUENCY = 600

READ_WEBSOCKET_DELAY = 0.1
WRITE_DELAY = 0.1

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'rotate': {
            'level': 'INFO',
            'formatter': 'verbose',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(PATH, '../logs/choboi.log'),
            'when': 'midnight',
            'backupCount': 7,
        }
    },
    'loggers': {
        '': {
            'handlers': ['console', 'rotate'],
            'level': 'INFO'
        }
    }
}
dictConfig(LOGGING)
