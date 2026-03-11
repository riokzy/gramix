from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from gramix.types.user import User

if TYPE_CHECKING:
    from gramix.bot import Bot

@dataclass(slots=True)
class InlineQueryResultArticle:
    id: str
    title: str
    message_text: str
    description: str | None = None
    parse_mode: str | None = None

    def to_dict(self) -> dict:
        result: dict = {
            "type": "article",
            "id": self.id,
            "title": self.title,
            "input_message_content": {
                "message_text": self.message_text,
            },
        }
        if self.description:
            result["description"] = self.description
        if self.parse_mode:
            result["input_message_content"]["parse_mode"] = self.parse_mode
        return result

@dataclass(slots=True)
class InlineQueryResultPhoto:
    id: str
    photo_url: str
    thumb_url: str
    title: str | None = None
    description: str | None = None
    caption: str | None = None
    parse_mode: str | None = None

    def to_dict(self) -> dict:
        result: dict = {
            "type": "photo",
            "id": self.id,
            "photo_url": self.photo_url,
            "thumbnail_url": self.thumb_url,
        }
        if self.title:
            result["title"] = self.title
        if self.description:
            result["description"] = self.description
        if self.caption:
            result["caption"] = self.caption
        if self.parse_mode:
            result["parse_mode"] = self.parse_mode
        return result

@dataclass(slots=True)
class InlineQueryResultGif:
    id: str
    gif_url: str
    thumb_url: str
    title: str | None = None
    caption: str | None = None
    parse_mode: str | None = None

    def to_dict(self) -> dict:
        result: dict = {
            "type": "gif",
            "id": self.id,
            "gif_url": self.gif_url,
            "thumbnail_url": self.thumb_url,
        }
        if self.title:
            result["title"] = self.title
        if self.caption:
            result["caption"] = self.caption
        if self.parse_mode:
            result["parse_mode"] = self.parse_mode
        return result

@dataclass(slots=True)
class InlineQueryResultVideo:
    id: str
    video_url: str
    mime_type: str
    thumb_url: str
    title: str
    caption: str | None = None
    parse_mode: str | None = None
    description: str | None = None

    def to_dict(self) -> dict:
        result: dict = {
            "type": "video",
            "id": self.id,
            "video_url": self.video_url,
            "mime_type": self.mime_type,
            "thumbnail_url": self.thumb_url,
            "title": self.title,
        }
        if self.caption:
            result["caption"] = self.caption
        if self.parse_mode:
            result["parse_mode"] = self.parse_mode
        if self.description:
            result["description"] = self.description
        return result

@dataclass(slots=True)
class InlineQueryResultDocument:
    id: str
    title: str
    document_url: str
    mime_type: str
    caption: str | None = None
    parse_mode: str | None = None
    description: str | None = None

    def to_dict(self) -> dict:
        result: dict = {
            "type": "document",
            "id": self.id,
            "title": self.title,
            "document_url": self.document_url,
            "mime_type": self.mime_type,
        }
        if self.caption:
            result["caption"] = self.caption
        if self.parse_mode:
            result["parse_mode"] = self.parse_mode
        if self.description:
            result["description"] = self.description
        return result

@dataclass(slots=True)
class InlineQueryResultAudio:
    id: str
    audio_url: str
    title: str
    caption: str | None = None
    parse_mode: str | None = None
    performer: str | None = None
    audio_duration: int | None = None

    def to_dict(self) -> dict:
        result: dict = {
            "type": "audio",
            "id": self.id,
            "audio_url": self.audio_url,
            "title": self.title,
        }
        if self.caption:
            result["caption"] = self.caption
        if self.parse_mode:
            result["parse_mode"] = self.parse_mode
        if self.performer:
            result["performer"] = self.performer
        if self.audio_duration:
            result["audio_duration"] = self.audio_duration
        return result

class InlineQuery:
    __slots__ = ("id", "from_user", "query", "offset", "_bot")

    def __init__(
        self,
        id: str,
        from_user: User,
        query: str,
        offset: str,
        bot: Bot,
    ) -> None:
        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset
        self._bot = bot

    def answer(
        self,
        results: list[InlineQueryResultArticle | InlineQueryResultPhoto | InlineQueryResultGif | InlineQueryResultVideo | InlineQueryResultDocument | InlineQueryResultAudio],
        *,
        cache_time: int = 300,
        is_personal: bool = False,
        next_offset: str | None = None,
    ) -> bool:
        return self._bot.answer_inline_query(
            inline_query_id=self.id,
            results=[r.to_dict() for r in results],
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
        )

    @classmethod
    def from_dict(cls, data: dict, bot: Bot) -> InlineQuery:
        return cls(
            id=data["id"],
            from_user=User.from_dict(data["from"]),
            query=data.get("query", ""),
            offset=data.get("offset", ""),
            bot=bot,
        )
