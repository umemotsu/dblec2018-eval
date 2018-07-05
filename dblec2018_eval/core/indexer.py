# -*- coding: utf-8 -*-


import collections
import logging


logger = logging.getLogger(__name__)


class Indexer:
    def __init__(self, tokenizer):
        self._tokenizer = tokenizer

    def index(self, page):
        page_index = self._index_page(page)
        link_indices = list(self._index_links(page))

        logger.debug(f'{len(page.title):,} title tokens, '
                     f'{len(page.body):,} body tokens, and '
                     f'{len(link_indices):,} outbound links in {page.url}')

        return page_index, link_indices

    def _index_page(self, page):
        title = self._tokenizer.tokenize(page.title)
        body = self._tokenizer.tokenize(page.body)

        return PageIndex(page.url, title, body)

    def _index_links(self, page):
        src = page.url

        for link in page.links:
            dest = link.url
            anchor = self._tokenizer.tokenize(link.text)

            yield LinkIndex(src, dest, anchor)


class IndexMixin:
    @classmethod
    def read(cls, fin):
        for line in fin:
            yield line.rstrip('\n').split('\t')

    @classmethod
    def concat(cls, words_list):
        return ' '.join(words_list)

    @classmethod
    def split(cls, words_str):
        return words_str.split(' ') if words_str else []

    def write(self, fout, elems):
        line = '\t'.join(elems)
        print(line, file=fout, flush=True)


class PageIndex(IndexMixin, collections.namedtuple('PageIndex', ['url', 'title', 'body'])):
    @classmethod
    def read(cls, fin):
        for elems in super().read(fin):
            url, title, body = elems

            yield cls(url, cls.split(title), cls.split(body))

    def write(self, fout):
        elems = [self.url, self.concat(self.title), self.concat(self.body)]
        super().write(fout, elems)


class LinkIndex(IndexMixin, collections.namedtuple('LinkIndex', ['src', 'dest', 'anchor'])):
    @classmethod
    def read(cls, fin):
        for elems in super().read(fin):
            src, dest, anchor = elems

            yield cls(src, dest, cls.split(anchor))

    def write(self, fout):
        elems = [self.src, self.dest, self.concat(self.anchor)]
        super().write(fout, elems)
