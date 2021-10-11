from __future__ import annotations

import typing

from aiohttp import web

if typing.TYPE_CHECKING:
    from .router import Router
    from .manager import Manager

class Server:
    def __init__(
        self,
        manager: typing.Type[Manager],
        router: typing.Type[Router],
    ) -> None:
        self.manager = manager(self)
        self.router = router(self)

        self.app: typing.Optional[web.Application] = None

    def reset(self) -> None:
        pass

    def setup(self) -> None:
        self.app = app = web.Application()
        app.add_routes(self.router.routes)

    def run(self, **options: typing.Any) -> None:
        self.reset()
        self.setup()

        assert self.app
        web.run_app(self.app, **options)
