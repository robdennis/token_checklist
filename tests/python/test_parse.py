# -*- coding: utf8 -*-
"""
:mod:`test_parse` -- tests related to parsing the text of cards
"""
from __future__ import unicode_literals
import itertools

import pytest
from token_checklist import get_makers
from token_checklist.token_parser import Token, TokenParser


@pytest.fixture(scope='session')
def token_makers():
    return get_makers()


@pytest.fixture(scope='session')
def token_parser(token_makers):
    return TokenParser(token_makers)


@pytest.fixture(scope='session')
def parse_card(token_parser):
    return token_parser.get_tokens


@pytest.fixture(scope='session')
def dump_cards(token_parser):
    return token_parser.dump_all_tokens


class TestDumpingTokens(object):
    def assert_index_equal(self, index, actual, expected):
        # index is brought in specifically to be show in py.test's error
        # traceback
        assert actual == expected

    def assert_cards_in_order(self, actual, expected_cards):
        assert len(actual) == len(expected_cards)

        for actual, expected, idx in itertools.izip(
            actual, (dict(card._asdict()) for card in expected_cards),
            itertools.count()
        ):
            self.assert_index_equal(idx, actual, expected)

    def test_simple(self, dump_cards, saproling, myr, ooze):
        self.assert_cards_in_order(
            dump_cards(['Sprout', 'Genesis Chamber', 'Miming Slime']),
            [saproling, myr, ooze]
        )

    def test_deduping(self, dump_cards, saproling, squirrel):
        self.assert_cards_in_order(
            dump_cards(['Sprout', 'Sprout', 'Sprout']),
            [saproling]
        )

        self.assert_cards_in_order(
            dump_cards(['Sprout', 'Squirrel Nest', 'Thallid']),
            [saproling, squirrel]
        )


class TestBreakdownRulesText(object):

    def assert_expected_number_of_snippets(self, card_text, expected):
        assert len(TokenParser._get_snippets(card_text)) == expected

    def assert_token_from_snippet(self, snippet, expected):
        assert TokenParser._get_token_from_snippet(snippet) == expected

    def test_has_tokens(self, token_parser, sprout_text):
        assert token_parser._has_tokens(sprout_text)
        assert not token_parser._has_tokens('')

    def test_got_snippets(self, token_parser, sprout_text, doj_text,
                          bestial_menace_text):
        self.assert_expected_number_of_snippets(sprout_text, 1)
        self.assert_expected_number_of_snippets(doj_text, 2)
        self.assert_expected_number_of_snippets(bestial_menace_text, 3)

    def test_get_token_from_sprout_snippet(self, sprout_text, saproling):
        snippets = TokenParser._get_snippets(sprout_text)
        self.assert_token_from_snippet(snippets[0], saproling)

    def test_get_token_from_decree_snippet(self, doj_text, soldier, angel):
        snippets = TokenParser._get_snippets(doj_text)
        self.assert_token_from_snippet(snippets[0], angel)
        self.assert_token_from_snippet(snippets[1], soldier)

    def test_get_token_from_menace_snippet(self, bestial_menace_text,
                                           snake, wolf, elephant):
        snippets = TokenParser._get_snippets(bestial_menace_text)
        self.assert_token_from_snippet(snippets[0], snake)
        self.assert_token_from_snippet(snippets[1], wolf)
        self.assert_token_from_snippet(snippets[2], elephant)

    def test_get_token_from_gutter_grime_snippet(self, gutter_grime_text,
                                                 gutter_grime):
        snippets = TokenParser._get_snippets(gutter_grime_text)
        self.assert_token_from_snippet(snippets[0], gutter_grime)


class TestTokensFromCards(object):

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

    def test_multi_color_and_multi_class(self, parse_card, rg_goblin_warrior):
        assert parse_card('Wort, the Raidmother') == [rg_goblin_warrior]
        assert parse_card('Mercy Killing') == [Token('Elf Warrior', '1/1',
                                                     'green and white')]

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

    def test_multiple_tokens(self, parse_card, wolf, elephant):
        assert parse_card("One Dozen Eyes") == [
            Token('Beast', '5/5', 'green'),
            Token('Insect', '1/1', 'green'),
        ]

        assert parse_card("Bestial Menace") == [
            Token('Snake', '1/1', 'green'),
            wolf,
            elephant,
        ]

    def test_tokens_with_abilities(self, parse_card):
        assert parse_card("Horncaller's Chant") == [
            Token('Rhino', '4/4', 'green', abilities='trample'),
        ]

        assert parse_card("Spider Spawning") == [
            Token('Spider', '1/2', 'green', abilities='reach'),
        ]

    def test_tokens_with_multiple_abilities(self, parse_card):
        assert parse_card("Hornet Queen") == [
            Token('Insect', '1/1', 'green', abilities='flying and deathtouch')
        ]

    def test_multiple_tokens_with_abilities(self, parse_card):
        assert parse_card("Trostani's Summoner") == [
            Token('Knight', '2/2', 'white', abilities='vigilance'),
            Token('Centaur', '3/3', 'green'),
            Token('Rhino', '4/4', 'green', abilities='trample'),
        ]

    def test_tokens_that_generate_tokens(self, parse_card):
        assert parse_card('Mitotic Slime') == [
            Token('Ooze', '2/2', 'green',
                  abilities=('"When this creature dies, put two 1/1 green '
                             'Ooze creature tokens onto the battlefield."')),
            Token('Ooze', '1/1', 'green')
        ]
