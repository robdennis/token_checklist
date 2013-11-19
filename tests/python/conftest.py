"""
Place test-wide fixtures here
"""
import pytest
from token_checklist.token_parser import Token


@pytest.fixture
def saproling():
    return Token('Saproling', '1/1', 'green')


@pytest.fixture
def squirrel():
    return Token('Squirrel', '1/1', 'green')


@pytest.fixture
def golem():
    return Token('Golem', '3/3', 'colorless', extra_card_types='artifact')


@pytest.fixture
def myr():
    return Token('Myr', '1/1', 'colorless', extra_card_types='artifact')


@pytest.fixture
def ooze():
    return Token('Ooze', 'X/X', 'green')
