import time
import logging
import hashlib
import requests

from typing import Union, List

import utils

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def get_player_capture_url(player: utils.Player) -> str:
    str2hash = str(player.id) + player.secret_key + str(int(time.time()))
    result = hashlib.md5(str2hash.encode())
    return (
        f"https://www.futsell.ru/ffa19/api/pop/id/{player.id}/"
        f"ts/{int(time.time())}/sign/{result.hexdigest()}"
        f"/sku/FFA19PS4?min_buy={player.minimum_price}"
        f"&max_buy={player.maximum_price}"
    )


def check_response(response: requests.models.Response) -> bool:
    """Checks the answer to the player's capture."""
    context = response.json()
    if context["error"] == "":
        return True
    elif context["error"] == "AUTH":
        raise utils.AuthError
    else:
        return False


def validate_context_for_player(context: List[str]) -> List[Union[int, str]]:
    if len(context) != 5:
        raise utils.ListLengthError(context)

    context = [int(field) if field.isdigit() else field for field in context]
    return context


def working_hours(period: int, start: float) -> bool:
    """How long will requests to capture a player be sent.
    :param period: running time in minutes
    :param start: start time
    """
    period *= 60
    if (time.time() - start) > period:
        return True


def start_asking_player(player: utils.Player) -> str:
    """Sends requests to capture the player."""
    start_time = time.time()
    while True:
        try:
            time.sleep(1)
            url = get_player_capture_url(player)
            response = requests.get(url)
            logging.info((response.json(), time.ctime()))

            if check_response(response):
                return "Игрок взят"

            if working_hours(player.time, start_time):
                return "Время вышло"

        except Exception as e:
            logging.warning(e)
