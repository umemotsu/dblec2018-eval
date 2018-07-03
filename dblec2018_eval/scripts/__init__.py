# -*- coding: utf-8 -*-


import logging.config

import click

from .. import __name__ as pkg_name
from .utils import register


log_config = {
    'version': 1,
    'formatters': {
        'multi_line': {
            'format': '[%(asctime)s][%(name)s][%(funcName)s@%(filename)s:%(lineno)d][%(levelname)s]\n%(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'multi_line',
            'level': 'DEBUG',
            'stream': 'ext://sys.stderr'
        }
    },
    'loggers': {
        pkg_name: {
            'level': 'DEBUG',
            'handlers': ['console']
        }
    }
}


@click.group(help=f'Command Line Interface for the {pkg_name} package.')
@click.option('--log/--no-log', default=True, help='Whether to print logging messages (default: true).')
@click.version_option()
def cli(log):
    if log:
        logging.config.dictConfig(log_config)


register(cli, [])
