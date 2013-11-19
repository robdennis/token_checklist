"""
:mod:`token_checklist` -- Given a List of Magic: The Gathering Card names, \
return a list of tokens produced
"""
from __future__ import unicode_literals, print_function
import os
import json

from flask import Flask, send_file, request

from . import metadata, token_parser

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright
__here__ = os.path.abspath(os.path.dirname(__file__))


def get_makers():
    json_file = os.path.join(__here__, 'token_makers.json')
    return json.load(open(json_file, 'rb'))


_parser = token_parser.TokenParser(get_makers())
app = Flask(__name__)


@app.route('/')
def check():
    return send_file('templates/index.html')


@app.route('/list', methods=['POST'])
def consume_cards():
    if request.method == 'POST':
        print(request.data)
    return json.dumps([_parser.get_tokens(name, to_dict=True)
                       for name in request.data.splitlines()])
