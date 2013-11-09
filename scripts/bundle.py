import json
import os

__here__ = os.path.abspath(os.path.dirname(__file__))

# generated from gather.py
CARDS_JSON = os.path.join(__here__, 'cards.json')
TOKEN_JSON = os.path.join(__here__, '..', 'token_checklist', 'static',
                          'token_makers.json')


def write_subset_of_cards_to_file(all_cards):

    cards = {
        card['name']: card['text'] for card in all_cards.itervalues()
        # as a naive sanity check
        if 'token' in card.get('text', '')
    }

    json.dump(cards, open(TOKEN_JSON, 'wb'), indent=2)

if __name__ == '__main__':
    write_subset_of_cards_to_file(json.load(open(CARDS_JSON)))
