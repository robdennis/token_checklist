"""
:mod:`token_checklist` -- Given a List of Magic: The Gathering Card names, \
return a list of tokens produced
"""
from __future__ import unicode_literals
import os
import re
import json
from collections import namedtuple

from flask import Flask, send_file

from token_checklist import metadata

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


def parse_card(card_name, all_cards):
    """
    :param card_name: the name of the card to parse
    :return: a list of all token types found on the card
    :rtype: list
    """

    return parse(all_cards.get(card_name, ''))


def parse(card_text):
    color_group = '(?:white|blue|black|red|green|colorless)'
    type_group = '(?:artifact|enchantment)'
    pattern = """
        puts?\s                       # 'put' is a key part of this template
        .+?\s                         # and we don't care about the number
        # it's optional for the */* case and if it's X, it's always(?)
        # X for both power and toughness
        (?P<stats>(\d|X)+/(\d+|X))?\s?
        # pick of things like 'white blue and black'
        (?P<color>{color_group}((\s|\sand\s){color_group})*)\s
        (?P<creature_types>.+?)\s     # these are always capitalized FWIW
        # pick of things like 'artifact enchantment'
        (?P<extra_card_types>{type_group}((\s|\sand\s){type_group})*)?\s?
        creature\stokens?\sonto\sthe\sbattlefield(\s|\.)*
        # optional abilities that are either:
        # - 'with (or they have) reach and first strike'
        # or
        # - 'with (or they have) "ability text."'
		(?:(with|they\shave)\s(?P<abilities>(".*?")|([^"].+[^.])))?
    """.format(color_group=color_group,
               type_group=type_group)
    return [
        Token(**match.groupdict())
        for match in re.finditer(pattern, card_text, re.I | re.X)
    ]


app = Flask(__name__)

@app.route('/')
def check():
    return send_file('templates/index.html')
