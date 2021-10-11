from __future__ import annotations

import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from .server import Server


@dataclass
class Game:
    id_: str


class Manager:
    def __init__(self, server: Server) -> None:
        self.server = server

    def get_game(self, id_: str) -> typing.Optional[Game]:
        return Game(id_)
