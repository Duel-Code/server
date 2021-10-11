from __future__ import annotations

import typing
import inspect

from aiohttp.web import Request, Response, RouteDef

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
