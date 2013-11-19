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
                name=None, extra_card_types=None, abilities=None,
                first_ability_block=None, second_ability_block=None):
        """
        To support some default arguments
        """
        if not abilities:
            actual_abilities = ((first_ability_block or '') +
                                (second_ability_block or ''))
            if '"' not in actual_abilities:
                # naive check for normalize all keyword abilities
                actual_abilities = actual_abilities.lower()
        else:
            # this only really comes up in test data
            actual_abilities = abilities

        kwargs = dict(
            creature_types=creature_types, stats=stats or '*/*',
            color=color.lower(), name=name or creature_types,
            extra_card_types=extra_card_types or '',
            abilities=actual_abilities
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

        return list(self.parse(self.card_mapping.get(card_name, '')))

    @staticmethod
    def _has_tokens(card_text):
        """
        Are there tokens to be found in this card?
        :param card_text:
        :return: True if there are tokens, else, False
        """

        return re.search('puts?[^.]+tokens?[^.]+onto the battlefield',
                         card_text, re.I)

    @staticmethod
    def _get_snippets(card_text):
        pattern = (r'([^.,]*?creature token[^.,;]*'
                   r'(?:\. They[^.]+have[^.]+)?(?:\."?)?)')

        return re.findall(pattern, card_text, re.I)

    @staticmethod
    def _get_token_from_snippet(snippet):
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
            creature\stokens?\s?
            # sometimes abilities are before the "onto the battlefield"
            (?:with\s(?P<first_ability_block>.+?))?\s?
            (?:,|onto\sthe\sbattlefield|$)\.?\s?
            # sometimes after
            (?:(?:with|they\shave)\s(?P<second_ability_block>".+?"))?
        """

        match = re.search(pattern, snippet, re.I | re.X)
        if match:
            return Token(**match.groupdict())
        else:
            return None

    @staticmethod
    def parse(card_text):
        """
        :param card_text: the string content of a the card you want to check
        :return: all tokens (if they appear) as a list of Token namedtuples
        """
        if not TokenParser._has_tokens(card_text):
            # sanity check
            return []

        def yield_tokens_from_snippets():
            for snippet in TokenParser._get_snippets(card_text):
                found_token = TokenParser._get_token_from_snippet(snippet)
                if found_token is not None:
                    yield found_token
                    if TokenParser._has_tokens(found_token.abilities):
                        yield TokenParser._get_token_from_snippet(
                            found_token.abilities
                        )

        return yield_tokens_from_snippets()
