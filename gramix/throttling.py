from __future__ import annotations
import asyncio
import time
from collections.abc import Callable
from typing import Any


class ThrottlingMiddleware:
    """Rate-limiting middleware.

    Limits how often a single user can trigger handlers.
    Works transparently in both sync and async modes.

    Args:
        rate: Minimum seconds between accepted messages per user. Default: 1.0.
        on_throttle: Optional callback ``(update) -> None`` (or async) called
            when a message is throttled.  If *None*, throttled messages are
            silently dropped.

    Usage::

        from gramix import ThrottlingMiddleware

        dp.middleware(ThrottlingMiddleware(rate=1.0))

        # With a custom throttle handler:
        def on_throttle(msg):
            msg.answer("⚠️ Слишком много запросов. Подождите секунду.")

        dp.middleware(ThrottlingMiddleware(rate=1.0, on_throttle=on_throttle))
    """

    def __init__(
        self,
        rate: float = 1.0,
        on_throttle: Callable | None = None,
    ) -> None:
        self._rate = rate
        self._on_throttle = on_throttle
        self._last_seen: dict[int, float] = {}

    def _get_key(self, update: Any) -> int | None:
        """Extract a per-user key from the update object."""
        from_user = getattr(update, "from_user", None)
        if from_user is not None:
            return getattr(from_user, "id", None)
        chat = getattr(update, "chat", None)
        if chat is not None:
            return getattr(chat, "id", None)
        return None

    def _is_throttled(self, key: int) -> bool:
        now = time.monotonic()
        last = self._last_seen.get(key)
        if last is None or (now - last) >= self._rate:
            self._last_seen[key] = now
            return False
        return True

    # ── sync interface ────────────────────────────────────────────────────────

    def __call__(self, update: Any, next_fn: Callable) -> None:
        key = self._get_key(update)
        if key is not None and self._is_throttled(key):
            if self._on_throttle is not None:
                if asyncio.iscoroutinefunction(self._on_throttle):
                    # best-effort: run async callback from sync context
                    try:
                        loop = asyncio.get_event_loop()
                        if loop.is_running():
                            loop.create_task(self._on_throttle(update))
                        else:
                            loop.run_until_complete(self._on_throttle(update))
                    except RuntimeError:
                        asyncio.run(self._on_throttle(update))
                else:
                    self._on_throttle(update)
            return
        next_fn()

    # ── async interface (same object, detected by iscoroutinefunction) ────────

    async def async_call(self, update: Any, next_fn: Callable) -> None:
        key = self._get_key(update)
        if key is not None and self._is_throttled(key):
            if self._on_throttle is not None:
                if asyncio.iscoroutinefunction(self._on_throttle):
                    await self._on_throttle(update)
                else:
                    self._on_throttle(update)
            return
        if asyncio.iscoroutinefunction(next_fn):
            await next_fn()
        else:
            next_fn()
