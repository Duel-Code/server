from __future__ import annotations

import typing
import inspect
from dataclasses import asdict

from aiohttp.web import Request, Response, RouteDef
from aiohttp.web_response import json_response

if typing.TYPE_CHECKING:
    from ..server import Server

F = typing.Callable[..., typing.Any]
T = typing.TypeVar('T', bound=F)


def route(method: str, path: str, **kwargs: typing.Any) -> F:
    method = method.upper()

    def decorator(f: T) -> T:
        f._route_ = {  # type: ignore
            "path": path,
            "method": method,
            "kwargs": kwargs,
        }
        return f

    return decorator


class Router:
    __routes__: typing.List[RouteDef]

    def __init__(self, server: Server) -> None:
        self.server = server
        self.manager = server.manager

    @property
    def routes(self) -> typing.Generator[RouteDef, None, None]:
        yield from (
            RouteDef(handler=f, **f._route_)
            for _, f in inspect.getmembers(self)
            if hasattr(f, "_route_")
        )

    @route(method="GET", path='/')
    async def index(self, request: Request) -> Response:
        return Response(body="Hello, World!")

    @route(method="GET", path="/games")
    async def list_games(self, request: Request) -> Response:
        data = []
        return json_response(data)

    @route(method="GET", path="/games/{id}")
    async def get_game(self, request: Request) -> Response:
        id_ = request.match_info["id"]

        game = self.manager.get_game(id_)
        if not game:
            return Response(text="Game not found", status=404)

        data = asdict(game)
        return json_response(data)
