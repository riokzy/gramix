from __future__ import annotations
from typing import TYPE_CHECKING

from gramix.types.user import User
from gramix.types.message import Message

if TYPE_CHECKING:
    from gramix.bot import Bot


class CallbackQuery:
    __slots__ = ("id", "from_user", "message", "data", "inline_message_id", "_bot")

    def __init__(
        self,
        id: str,
        from_user: User,
        message: Message | None,
        data: str | None,
        inline_message_id: str | None,
        bot: Bot,
    ) -> None:
        self.id = id
        self.from_user = from_user
        self.message = message
        self.data = data
        self.inline_message_id = inline_message_id
        self._bot = bot

    def answer(
        self,
        text: str | None = None,
        *,
        show_alert: bool = False,
        url: str | None = None,
        cache_time: int = 0,
    ) -> bool:
        return self._bot.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )

    @classmethod
    def from_dict(cls, data: dict, bot: Bot) -> CallbackQuery:
        return cls(
            id=data["id"],
            from_user=User.from_dict(data["from"]),
            message=Message.from_dict(data["message"], bot) if "message" in data else None,
            data=data.get("data"),
            inline_message_id=data.get("inline_message_id"),
            bot=bot,
        )
