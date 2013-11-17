"""
:mod:`token_checklist` -- Given a List of Magic: The Gathering Card names, \
return a list of tokens produced
"""
from __future__ import unicode_literals, print_function
import os
import re
import json
from collections import namedtuple

from flask import Flask, send_file, request

from . import metadata

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright
__here__ = os.path.abspath(os.path.dirname(__file__))


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
            extra_card_types=extra_card_types or [],
            abilities=abilities or []
        )
        return super(Token, cls).__new__(cls, **kwargs)


def get_makers():
    json_file = os.path.join(__here__, 'token_makers.json')
    return json.load(open(json_file, 'rb'))


def parse_card(card_name, all_cards, to_dict=False):
    """
    :param card_name: the name of the card to parse
    :param to_dict: is True, return dictionaries instead of named tuples
    :return: a list of all token types found on the card
    :rtype: list
    """

    all_parsed = parse(all_cards.get(card_name, ''))
    if to_dict:
        return [parsed._asdict()
                for parsed in all_parsed]
    else:
        return all_parsed


def parse(card_text):
    """
    :param card_text: the string content of a the card you want to check
    :return: all tokens (if they appear) as a list of Token namedtuples
    """

    if not re.search('puts?[^.]+tokens?[^.]+onto the battlefield', card_text,
                     re.I):
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

_makers = get_makers()
app = Flask(__name__)


@app.route('/')
def check():
    return send_file('templates/index.html')


@app.route('/list', methods=['POST'])
def consume_cards():
    if request.method == 'POST':
        print(request.data)
    return json.dumps([parse_card(name, _makers)
                       for name in request.data.splitlines()])
