# -*- coding: utf8 -*-
"""
:mod:`token_parser` -- Handle the task of parsing token-relevant information
from a card
"""
from __future__ import unicode_literals, print_function
from itertools import ifilterfalse, chain

import re
from collections import namedtuple


def unique_everseen(iterable, key=None):
    """
    List unique elements, preserving order. Remember all elements ever seen.
    http://docs.python.org/2/library/itertools.html#recipes
    """
    # unique_everseen('AAAABBBCCDAABBB') --> A B C D
    # unique_everseen('ABBCcAD', str.lower) --> A B C D
    seen = set()
    seen_add = seen.add
    if key is None:
        for element in ifilterfalse(seen.__contains__, iterable):
            seen_add(element)
            yield element
    else:
        for element in iterable:
            k = key(element)
            if k not in seen:
                seen_add(k)
                yield element


class Token(namedtuple('Token', 'creature_types stats color name '
                                'extra_card_types abilities')):
    def __new__(cls, creature_types, stats, color,
                name=None, extra_card_types=None, abilities=None):
        """
        To support some default arguments
        """
        kwargs = dict(
            creature_types=creature_types, stats=stats or '*/*',
            color=color.lower(), name=name or creature_types,
            extra_card_types=extra_card_types or '',
            abilities=abilities or ''
        )
        return super(Token, cls).__new__(cls, **kwargs)


class TokenParser(object):
    def __init__(self, card_mapping):
        self.card_mapping = card_mapping

    def dump_all_tokens(self, card_names):
        """
        :param card_names: a list of (potential) card names
        :return: a list of dictionaries representing tokens found using
            card_names, this is not de-duplicated
        """
        all_tokens = (
            self.get_tokens(name) for name in card_names
        )

        return [
            dict(unique_token._asdict())
            for unique_token in unique_everseen(chain(*all_tokens))
        ]

    def get_tokens(self, card_name):
        """
        :param card_name: the name of the card to parse
        :return: a list of all token types found on the card as Token
            namedtuples
        :rtype: list
        """

        return self.parse(self.card_mapping.get(card_name, ''))

    @staticmethod
    def parse(card_text):
        """
        :param card_text: the string content of a the card you want to check
        :return: all tokens (if they appear) as a list of Token namedtuples
        """
        if not re.search('puts?[^.]+tokens?[^.]+onto the battlefield',
                         card_text, re.I):
            # sanity check
            return []

        pattern = """
            # it's optional for the */* case and if it's X, it's always(?)
            # X for both power and toughness
            (?P<stats>(\d|X)+/(\d+|X))?\s?
            # pick of things like 'white blue and black'
            (?P<color>(?:white|blue|black|red|green|colorless)((\s|\sand\s)
            (?:white|blue|black|red|green|colorless))*)\s
            (?P<creature_types>.+?)\s     # these are always capitalized FWIW
            # pick of things like 'artifact enchantment'
            (?P<extra_card_types>(?:artifact|enchantment)
            ((\s|\sand\s)(?:artifact|enchantment))*)?\s?
            creature\stokens?
            # it may be comma delimited due to multiple tokens
            (\sonto\sthe\sbattlefield(\s|\.)*)?
            # optional abilities that are either:
            # - 'with (or they have) reach and first strike'
            # or
            # - 'with (or they have) "ability text."'
            (?:(with|they\shave)\s(?P<abilities>(".*?")|([^"].+[^.])))?
        """

        return [
            Token(**match.groupdict())
            for match in re.finditer(pattern, card_text, re.I | re.X)
        ]
