from __future__ import annotations

import enum
import typing
from datetime import datetime
from dataclasses import dataclass, field

if typing.TYPE_CHECKING:
    from .server import Server

_ = enum.auto


def random_game_id() -> str:
    dt = datetime.now()
    dt = dt.strftime("%H%M%S%f")
    dt = int(dt)
    return hex(dt)[2:]


class Language(enum.IntEnum):
    PYTHON = _()
    JAVASCRIPT = _()


class State(enum.IntEnum):
    WAITING = _()
    STARTING = _()
    RUNNING = _()
    FINISHED = _()
    TIMEOUT = _()


@dataclass
class User:
    name: str
    language: Language
    disconnected: bool = field(default=False)


@dataclass
class Game:
    id_: str = field(default_factory=random_game_id)
    state: State = field(default=State.WAITING)
    users: typing.List[User] = field(default_factory=list)


class Manager:
    def __init__(self, server: Server) -> None:
        self.server = server

    def get_game(self, id_: str) -> typing.Optional[Game]:
        return Game(id_)
