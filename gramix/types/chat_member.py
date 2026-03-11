from __future__ import annotations
from dataclasses import dataclass

from gramix.types.user import User
from gramix.types.chat import Chat

@dataclass(slots=True)
class ChatMemberUpdated:
    chat: Chat
    from_user: User
    date: int
    old_status: str
    new_status: str
    user: User

    @property
    def joined(self) -> bool:
        return self.new_status in ("member", "administrator", "creator") and\
               self.old_status in ("left", "kicked", "restricted")

    @property
    def left(self) -> bool:
        return self.new_status in ("left", "kicked") and\
               self.old_status in ("member", "administrator", "creator", "restricted")

    @classmethod
    def from_dict(cls, data: dict) -> ChatMemberUpdated:
        old_member = data.get("old_chat_member", {})
        new_member = data.get("new_chat_member", {})

        raw_user = new_member.get("user") or old_member.get("user")
        if raw_user is None:

            raw_user = {"id": 0, "is_bot": False, "first_name": "Unknown"}
        return cls(
            chat=Chat.from_dict(data["chat"]),
            from_user=User.from_dict(data["from"]),
            date=data["date"],
            old_status=old_member.get("status", "left"),
            new_status=new_member.get("status", "left"),
            user=User.from_dict(raw_user),
        )
