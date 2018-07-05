# -*- coding: utf-8 -*-


import collections
import itertools
import logging
import time
from urllib.parse import urldefrag, urljoin

import requests
import bs4


logger = logging.getLogger(__name__)


class Spider:
    def __init__(self, timeout=None, sleep=None):
        self._timeout = timeout
        self._sleep = sleep

    def walk(self, start_url, max_depth=None):
        crawled_urls = set()
        target_urls = {start_url}
        depth_iterable = itertools.count() if max_depth is None else range(max_depth)

        for depth in depth_iterable:
            logger.info(f'Crawling {len(target_urls):,} URLs at depth-{depth:,}...')
            new_target_urls = set()

            for url in target_urls:
                html = self._crawl(url)
                crawled_urls.add(url)

                if not html:
                    continue

                page = Page.parse(url, html)

                yield page

                for link in page.links:
                    link_url = link.url

                    if link_url not in crawled_urls:
                        new_target_urls.add(link_url)

                self._wait()

            target_urls = new_target_urls

    def _crawl(self, url):
        try:
            response = requests.get(url, timeout=self._timeout)
            response.encoding = response.apparent_encoding
        except requests.RequestException as e:
            logger.warning(f'Cannot access ({e.__class__.__name__}): {url}')
            return None

        if not response.ok:
            logger.warning(f'Bad status ({response.status_code}): {url}')
            return None

        if 'text/html' not in response.headers.get('Content-Type', ''):
            logger.info(f'Not HTML resource: {url}')
            return None

        return response.text

    def _wait(self):
        if self._sleep:
            time.sleep(self._sleep)


class Page(collections.namedtuple('Page', ['url', 'html', 'title', 'body', 'links'])):
    @classmethod
    def parse(cls, url, html, parser='html.parser'):
        soup = bs4.BeautifulSoup(html, parser)
        cls._clean(soup)
        title = cls._parse_title(soup)
        body = cls._parse_body(soup)
        links = list(cls._parse_links(soup, url))

        return Page(url, html, title, body, links)

    @classmethod
    def _clean(cls, soup):
        def remove(elems):
            for e in elems:
                e.extract()

        remove(soup('script'))
        remove(soup('style'))
        remove(soup(text=lambda e: isinstance(e, bs4.Comment)))

    @classmethod
    def _parse_title(cls, soup):
        return soup.title.text.strip() if soup.title else ''

    @classmethod
    def _parse_body(cls, soup):
        return soup.body.text.strip() if soup.body else ''

    @classmethod
    def _parse_links(cls, soup, base_url):
        for e in soup('a'):
            rel_url = e.attrs.get('href', '').strip()

            if not rel_url:
                continue

            url = urldefrag(urljoin(base_url, rel_url)).url
            text = e.text

            yield Link(url, text)


Link = collections.namedtuple('Link', ['url', 'text'])
