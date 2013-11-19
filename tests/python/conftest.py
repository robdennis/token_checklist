"""
Place test-wide fixtures here
"""
import pytest
from token_checklist.token_parser import Token


@pytest.fixture
def soldier():
    return Token('Soldier', '1/1', 'white')


@pytest.fixture
def angel():
    return Token('Angel', '4/4', 'white', abilities='flying')


@pytest.fixture
def saproling():
    return Token('Saproling', '1/1', 'green')


@pytest.fixture
def squirrel():
    return Token('Squirrel', '1/1', 'green')


@pytest.fixture
def snake():
    return Token('Snake', '1/1', 'green')


@pytest.fixture
def wolf():
    return Token('Wolf', '2/2', 'green')


@pytest.fixture
def elephant():
    return Token('Elephant', '3/3', 'green')


@pytest.fixture
def golem():
    return Token('Golem', '3/3', 'colorless', extra_card_types='artifact')


@pytest.fixture
def myr():
    return Token('Myr', '1/1', 'colorless', extra_card_types='artifact')


@pytest.fixture
def ooze():
    return Token('Ooze', 'X/X', 'green')


@pytest.fixture
def gutter_grime():
    return Token('Ooze', '*/*', 'green',
                 abilities=('"This creature\'s power and toughness are '
                            'each equal to the number of slime counters '
                            'on Gutter Grime."'))


@pytest.fixture
def gutter_grime_text(token_makers):
    return token_makers['Gutter Grime']


@pytest.fixture
def sprout_text(token_makers):
    return token_makers['Sprout']


@pytest.fixture
def doj_text(token_makers):
    return token_makers['Decree of Justice']


@pytest.fixture
def bestial_menace_text(token_makers):
    return token_makers['Bestial Menace']
