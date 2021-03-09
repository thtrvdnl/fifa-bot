from dataclasses import dataclass


@dataclass
class Player:
    id: int
    secret_key: str
    minimum_price: int
    maximum_price: int


class ListLengthError(ValueError):
    """ Context list of wrong length. """


class AuthError(ValueError):
    """ Incorrect user data. """
