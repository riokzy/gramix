import asyncio
import pytest
from gramix.middleware import MiddlewareManager


def test_middleware_runs_handler():
    mgr = MiddlewareManager()
    called = []

    def handler(upd):
        called.append(upd)

    mgr.run("msg", handler)
    assert called == ["msg"]


def test_middleware_chain_order():
    mgr = MiddlewareManager()
    order = []

    def mw1(upd, next_fn):
        order.append(1)
        next_fn()

    def mw2(upd, next_fn):
        order.append(2)
        next_fn()

    mgr.register(mw1)
    mgr.register(mw2)
    mgr.run("x", lambda upd: order.append("h"))
    assert order == [1, 2, "h"]


def test_middleware_can_block_handler():
    mgr = MiddlewareManager()
    called = []

    def blocking(upd, next_fn):
        pass

    mgr.register(blocking)
    mgr.run("x", lambda upd: called.append(True))
    assert called == []


def test_middleware_register_returns_func():
    mgr = MiddlewareManager()

    def mw(upd, next_fn):
        next_fn()

    result = mgr.register(mw)
    assert result is mw


@pytest.mark.asyncio
async def test_async_middleware_runs_handler():
    mgr = MiddlewareManager()
    called = []

    async def handler(upd):
        called.append(upd)

    await mgr.async_run("msg", handler)
    assert called == ["msg"]


@pytest.mark.asyncio
async def test_async_middleware_chain():
    mgr = MiddlewareManager()
    order = []

    async def mw1(upd, next_fn):
        order.append(1)
        await next_fn()

    async def mw2(upd, next_fn):
        order.append(2)
        await next_fn()

    mgr.register(mw1)
    mgr.register(mw2)

    async def handler(upd):
        order.append("h")

    await mgr.async_run("x", handler)
    assert order == [1, 2, "h"]


@pytest.mark.asyncio
async def test_async_middleware_can_block():
    mgr = MiddlewareManager()
    called = []

    async def blocking(upd, next_fn):
        pass

    mgr.register(blocking)

    async def handler(upd):
        called.append(True)

    await mgr.async_run("x", handler)
    assert called == []
