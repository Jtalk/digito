import os
from logging import config

_FORMAT = os.environ.get(
    'LOGGER_FORMAT', '%(asctime)s [%(levelname)s] (%(name)s): %(message)s')
_LEVEL = os.environ.get('LOGGER_LEVEL', 'INFO')

global _LOGCONF_INIT
_LOGCONF_INIT = False


def init_logs():
    config.dictConfig({
        'version': 1,
        'formatters': {
            'standard': {
                'format': _FORMAT,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': 'ext://sys.stdout'
            },
        },
        'root': {
            'level': _LEVEL,
            'handlers': ['console']
        }
    })


if not _LOGCONF_INIT:
    init_logs()
    _LOGCONF_INIT = True
