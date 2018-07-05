# -*- coding: utf-8 -*-


import logging.config

import click

from .. import __name__ as pkg_name
from .tasks import build_dataset
from .utils import register


@click.group(help=f'Command Line Interface for the {pkg_name} package.')
@click.option('--log/--no-log', default=True, help='Whether to print logging messages (default: true).')
@click.option('-l', '--level', default='INFO', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']),
              help='Level above which events are logged (default: INFO).')
@click.version_option()
def cli(log, level):
    if log:
        config = {
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
                    'level': level,
                    'handlers': ['console']
                }
            }
        }

        logging.config.dictConfig(config)


register(cli, [build_dataset])
