# -*- coding: utf-8 -*-


import abc

import MeCab


class Tokenizer(abc.ABC):
    @abc.abstractmethod
    def tokenize(self, text):
        return []


class MeCabTokenizer(Tokenizer):
    def __init__(self):
        self._mecab = MeCab.Tagger()
        self._mecab.parse('')  # to avoid target text being deallocated by GC during tokenization

    def tokenize(self, text):
        return list(self._tokenize(text))

    def _tokenize(self, text):
        node = self._mecab.parseToNode(text)

        if not node:
            return

        node = node.next

        while node.next:
            yield node.surface

            node = node.next
