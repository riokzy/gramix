import asyncio
import time
import pytest
from gramix.throttling import ThrottlingMiddleware


class _Msg:
    def __init__(self, user_id: int) -> None:
        self.from_user = _User(user_id)


class _User:
    def __init__(self, user_id: int) -> None:
        self.id = user_id


def test_first_message_passes():
    mw = ThrottlingMiddleware(rate=1.0)
    called = []
    mw(_Msg(1), lambda: called.append(1))
    assert called == [1]


def test_second_message_throttled():
    mw = ThrottlingMiddleware(rate=10.0)
    calls = []
    mw(_Msg(1), lambda: calls.append(1))
    mw(_Msg(1), lambda: calls.append(2))
    assert calls == [1]


def test_different_users_not_throttled():
    mw = ThrottlingMiddleware(rate=10.0)
    calls = []
    mw(_Msg(1), lambda: calls.append(1))
    mw(_Msg(2), lambda: calls.append(2))
    assert calls == [1, 2]


def test_passes_after_rate_expires():
    mw = ThrottlingMiddleware(rate=0.05)
    calls = []
    mw(_Msg(1), lambda: calls.append(1))
    time.sleep(0.1)
    mw(_Msg(1), lambda: calls.append(2))
    assert calls == [1, 2]


def test_on_throttle_sync_called():
    throttled = []
    mw = ThrottlingMiddleware(rate=10.0, on_throttle=lambda u: throttled.append(u))
    mw(_Msg(1), lambda: None)
    mw(_Msg(1), lambda: None)
    assert len(throttled) == 1


def test_get_key_falls_back_to_chat():
    class _ChatMsg:
        chat = _User(99)

    mw = ThrottlingMiddleware(rate=10.0)
    calls = []
    mw(_ChatMsg(), lambda: calls.append(1))
    assert calls == [1]


def test_get_key_none_always_passes():
    mw = ThrottlingMiddleware(rate=10.0)
    calls = []
    mw(object(), lambda: calls.append(1))
    mw(object(), lambda: calls.append(2))
    assert calls == [1, 2]


@pytest.mark.asyncio
async def test_async_call_passes():
    mw = ThrottlingMiddleware(rate=1.0)
    calls = []

    async def next_fn():
        calls.append(1)

    await mw.async_call(_Msg(10), next_fn)
    assert calls == [1]


@pytest.mark.asyncio
async def test_async_call_throttled():
    mw = ThrottlingMiddleware(rate=10.0)
    calls = []

    async def next_fn():
        calls.append(1)

    await mw.async_call(_Msg(10), next_fn)
    await mw.async_call(_Msg(10), next_fn)
    assert calls == [1]


@pytest.mark.asyncio
async def test_async_on_throttle_called():
    throttled = []

    async def on_throttle(u):
        throttled.append(u)

    mw = ThrottlingMiddleware(rate=10.0, on_throttle=on_throttle)

    async def next_fn():
        pass

    await mw.async_call(_Msg(5), next_fn)
    await mw.async_call(_Msg(5), next_fn)
    assert len(throttled) == 1
