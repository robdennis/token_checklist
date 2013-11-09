# -*- coding: utf8 -*-
"""
:mod:`test_parse` -- tests related to parsing the text of cards
"""
from __future__ import unicode_literals
from functools import partial
import pytest
from token_checklist import Token, parse_card


def test_sanity(token_makers):
    assert token_makers
    assert 'Sprout' in token_makers


class TestReturnedTokens(object):
    @pytest.fixture
    def saproling(self):
        return Token('Saproling', '1/1', 'green')

    @pytest.fixture
    def elf_warrior(self):
        return Token('Elf Warrior', '1/1', 'green')

    @pytest.fixture
    def rg_goblin_warrior(self):
        return Token('Goblin Warrior', '1/1', 'red and green')

    @pytest.fixture
    def hammer_golem(self):
        return Token('Golem', '3/3', 'colorless',
                     extra_card_types='enchantment artifact')

    @pytest.fixture
    def myr(self):
        return Token('Myr', '1/1', 'colorless',
                     extra_card_types='artifact')

    @pytest.fixture
    def ooze(self):
        return Token('Ooze', 'X/X', 'green')

    @pytest.fixture
    def gutter_grime(self):
        return Token('Ooze', '*/*', 'green',
                     abilities=('"This creature\'s power and toughness are '
                                'each equal to the number of slime counters '
                                'on Gutter Grime."'))

    @pytest.fixture
    def parse_card(self, token_makers):
        return partial(parse_card, all_cards=token_makers)

    def test_simple(self, parse_card, saproling):
        assert parse_card('Sprout') == [saproling]
        # makes 2 tokens
        assert parse_card('Bramble Elemental') == [saproling]
        # makes X tokens
        assert parse_card('Æther Mutation') == [saproling]

    def test_simple_race_and_class(self, parse_card, elf_warrior):
        assert parse_card('Gilt-Leaf Ambush') == [elf_warrior]
        assert parse_card('Hunting Triad') == [elf_warrior]
        assert parse_card('Imperious Perfect') == [elf_warrior]
        # this notably makes green AND WHITE Elf Warrior
        assert parse_card('Mercy Killing ') != [Token('Elf Warrior', '1/1',
                                                      'green and white')]

    def test_multi_color_and_multi_class(self, parse_card, rg_goblin_warrior):
        assert parse_card('Wort, the Raidmother') == [rg_goblin_warrior]

    def test_extra_types(self, parse_card, hammer_golem, myr):
        assert parse_card('Hammer of Purphoros') == [hammer_golem]
        assert parse_card('Genesis Chamber') == [myr]
        assert parse_card('Myr Incubator') == [myr]
        assert parse_card('Shrine of Loyal Legions') == [myr]

    def test_abilities_that_control_stats(self, parse_card, gutter_grime):
        assert parse_card('Gutter Grime') == [gutter_grime]

    def test_x_power(self, parse_card, ooze):
        assert parse_card('Slime Molding') == [ooze]
        assert parse_card('Gelatinous Genesis') == [ooze]
        assert parse_card('Miming Slime') == [ooze]

    def test_missing(self, parse_card):
        assert parse_card('Nonexistent') == []
        # this has the word token in it
        assert parse_card('Intangible Virtue') == []

    @pytest.mark.xfail
    def test_mitotic_slime(self, parse_card):

        assert parse_card('Mitotic Slime') == [
            Token('Ooze', '2/2', 'green',
                  abilities=('"When this creature dies, put two 1/1 green '
                              'Ooze creature tokens onto the battlefield."')),
            Token('Ooze', '1/1', 'green')
        ]