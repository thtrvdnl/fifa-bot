import time

import pytest

from requests.models import Response

import services
from utils import AuthError, ListLengthError


@pytest.mark.parametrize(
    "content, expected_result",
    [
        (b'{"error": ""}', True),
        (b'{"error": "EMPTY"}', False),
    ],
)
def test_check_response(content, expected_result):
    response = Response()
    response._content = content

    assert services.check_response(response) == expected_result


def test_check_response_auth():
    response = Response()
    response._content = b'{"error": "AUTH"}'

    with pytest.raises(AuthError):
        services.check_response(response)


def test_validate_context_for_player():
    context = ["123", "1b2dcde742bc1479e00665e42593cc68", "100", "200", "10"]
    assert services.validate_context_for_player(context) == [
        123,
        "1b2dcde742bc1479e00665e42593cc68",
        100,
        200,
        10,
    ]


@pytest.mark.parametrize("context", [[1, 2, 3, 4], [1, 2, 3, 4, 5, 6]])
def test_validate_context_for_player_raise(context):
    with pytest.raises(ListLengthError):
        services.validate_context_for_player(context)


@pytest.mark.parametrize(
    "period, start, expected_result",
    [
        (10, time.time(), None),
        (10, 0, True),
    ],
)
def test_working_hours(period, start, expected_result):
    assert services.working_hours(period, start) == expected_result


@pytest.fixture
def test_start_asking_player(player):
    assert services.start_asking_player(player) == "Время вышло"
