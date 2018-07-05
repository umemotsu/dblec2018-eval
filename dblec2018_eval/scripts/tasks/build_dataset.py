# -*- coding: utf-8 -*-


import logging

import click

from ...core.crawler import Crawler
from ...core.indexer import Indexer
from ...core.tokenizer import MeCabTokenizer


logger = logging.getLogger(__name__)


@click.command('build-dataset', help='Crawl and index web pages to build a dataset.')
@click.option('-t', '--timeout', type=float, default=10,
              help='Time in seconds to wait for response (default: 10 secs).')
@click.option('-s', '--sleep', type=float, default=1,
              help='Time in seconds to sleep before next request (default: 1 sec).')
@click.option('-p', '--progress-interval', type=int, default=100,
              help='When to report crawling progress (default: every 100 pages).')
@click.argument('start_url')
@click.argument('max_depth', type=int)
@click.argument('page_index_file', type=click.File('w'))
@click.argument('link_index_file', type=click.File('w'))
def build_dataset(timeout, sleep, progress_interval, start_url, max_depth, page_index_file, link_index_file):
    crawler = Crawler(timeout, sleep)
    indexer = Indexer(MeCabTokenizer())
    page_count = 0
    link_count = 0

    logger.info(f'Start crawling from {start_url} within {max_depth:,} link hops')

    for page in crawler.crawl(start_url, max_depth):
        page_index, link_indices = indexer.index(page)

        page_index.write(page_index_file)
        page_count += 1

        for link_index in link_indices:
            link_index.write(link_index_file)
            link_count += 1

        if page_count % progress_interval == 0:
            logger.info(f'Crawled {page_count:,} pages and {link_count:,} links thus far')

    logger.info(f'Crawled {page_count:,} pages and {link_count:,} links in total')
