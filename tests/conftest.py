import time

import pytest

from utils import Player


@pytest.fixture
def player():
    return Player(123, 1513454219, 999999, 999999, 1)
