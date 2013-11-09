import pytest
import token_checklist


@pytest.fixture(scope='session')
def token_makers():
    return token_checklist.get_makers()
