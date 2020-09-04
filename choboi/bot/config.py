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

THREAD_DELAY = 0.1

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://choboi:choboi@localhost:55432/choboi?sslmode=disable')

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
            'formatter': 'verbose'
        },
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO'
        }
    }
}
dictConfig(LOGGING)
