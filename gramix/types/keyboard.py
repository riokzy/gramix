from __future__ import annotations
from dataclasses import dataclass

from gramix.constants import MAX_CALLBACK_DATA_LENGTH

@dataclass(slots=True)
class InlineButton:
    text: str
    callback_data: str | None = None
    url: str | None = None
    switch_inline_query: str | None = None
    switch_inline_query_current_chat: str | None = None

    def to_dict(self) -> dict:
        btn: dict = {"text": self.text}
        if self.callback_data is not None:
            if len(self.callback_data) > MAX_CALLBACK_DATA_LENGTH:
                raise ValueError(
                    f"callback_data не должен превышать {MAX_CALLBACK_DATA_LENGTH} символов."
                )
            btn["callback_data"] = self.callback_data
        elif self.url is not None:
            btn["url"] = self.url
        elif self.switch_inline_query is not None:
            btn["switch_inline_query"] = self.switch_inline_query
        elif self.switch_inline_query_current_chat is not None:
            btn["switch_inline_query_current_chat"] = self.switch_inline_query_current_chat
        return btn

class Inline:
    def __init__(self) -> None:
        self._rows: list[list[InlineButton]] = [[]]

    def button(
        self,
        text: str,
        *,
        callback: str | None = None,
        url: str | None = None,
        switch_inline: str | None = None,
        switch_inline_current: str | None = None,
    ) -> Inline:
        self._rows[-1].append(
            InlineButton(
                text=text,
                callback_data=callback,
                url=url,
                switch_inline_query=switch_inline,
                switch_inline_query_current_chat=switch_inline_current,
            )
        )
        return self

    def row(self) -> Inline:
        if self._rows[-1]:
            self._rows.append([])
        return self

    def to_dict(self) -> dict:
        rows = [row for row in self._rows if row]
        return {"inline_keyboard": [[btn.to_dict() for btn in row] for row in rows]}

@dataclass(slots=True)
class ReplyButton:
    text: str
    request_contact: bool = False
    request_location: bool = False

    def to_dict(self) -> dict:
        btn: dict = {"text": self.text}
        if self.request_contact:
            btn["request_contact"] = True
        if self.request_location:
            btn["request_location"] = True
        return btn

class Reply:
    def __init__(
        self,
        *,
        resize: bool = True,
        one_time: bool = False,
        placeholder: str | None = None,
    ) -> None:
        self._rows: list[list[ReplyButton]] = [[]]
        self._resize = resize
        self._one_time = one_time
        self._placeholder = placeholder

    def button(self, text: str, *, contact: bool = False, location: bool = False) -> Reply:
        self._rows[-1].append(
            ReplyButton(text=text, request_contact=contact, request_location=location)
        )
        return self

    def row(self) -> Reply:
        if self._rows[-1]:
            self._rows.append([])
        return self

    def to_dict(self) -> dict:
        rows = [row for row in self._rows if row]
        result: dict = {
            "keyboard": [[btn.to_dict() for btn in row] for row in rows],
            "resize_keyboard": self._resize,
            "one_time_keyboard": self._one_time,
        }
        if self._placeholder:
            result["input_field_placeholder"] = self._placeholder
        return result

class RemoveKeyboard:
    def to_dict(self) -> dict:
        return {"remove_keyboard": True}

class BotCommand:
    __slots__ = ("command", "description")

    def __init__(self, command: str, description: str) -> None:
        if not command.startswith("/"):
            command = f"/{command}"
        self.command = command.lstrip("/")
        self.description = description

    def to_dict(self) -> dict:
        return {"command": self.command, "description": self.description}

    def __repr__(self) -> str:
        return f"BotCommand(/{self.command!r}, {self.description!r})"

class ChatPermissions:
    __slots__ = (
        "can_send_messages",
        "can_send_media_messages",
        "can_send_polls",
        "can_send_other_messages",
        "can_add_web_page_previews",
        "can_change_info",
        "can_invite_users",
        "can_pin_messages",
    )

    def __init__(
        self,
        *,
        can_send_messages: bool = False,
        can_send_media_messages: bool = False,
        can_send_polls: bool = False,
        can_send_other_messages: bool = False,
        can_add_web_page_previews: bool = False,
        can_change_info: bool = False,
        can_invite_users: bool = False,
        can_pin_messages: bool = False,
    ) -> None:
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_polls = can_send_polls
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_change_info = can_change_info
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages

    def to_dict(self) -> dict:
        return {
            "can_send_messages": self.can_send_messages,
            "can_send_media_messages": self.can_send_media_messages,
            "can_send_polls": self.can_send_polls,
            "can_send_other_messages": self.can_send_other_messages,
            "can_add_web_page_previews": self.can_add_web_page_previews,
            "can_change_info": self.can_change_info,
            "can_invite_users": self.can_invite_users,
            "can_pin_messages": self.can_pin_messages,
        }

    def __repr__(self) -> str:
        return f"ChatPermissions(can_send_messages={self.can_send_messages})"
