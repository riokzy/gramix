from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from gramix.types.user import User
from gramix.types.chat import Chat
from gramix.types.keyboard import Inline, Reply, RemoveKeyboard
from gramix.types.poll import Poll
from gramix.types.location import Location, Venue
from gramix.types.payment import SuccessfulPayment
from gramix.constants import MAX_MESSAGE_LENGTH, MAX_CAPTION_LENGTH, _SENTINEL
from gramix.exceptions import MessageError

if TYPE_CHECKING:
    from gramix.bot import Bot


@dataclass(slots=True)
class PhotoSize:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> PhotoSize:
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            width=data["width"],
            height=data["height"],
            file_size=data.get("file_size"),
        )


@dataclass(slots=True)
class Document:
    file_id: str
    file_unique_id: str
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Document:
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            file_name=data.get("file_name"),
            mime_type=data.get("mime_type"),
            file_size=data.get("file_size"),
        )


@dataclass(slots=True)
class Audio:
    file_id: str
    file_unique_id: str
    duration: int
    performer: str | None = None
    title: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Audio:
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            duration=data["duration"],
            performer=data.get("performer"),
            title=data.get("title"),
            file_name=data.get("file_name"),
            mime_type=data.get("mime_type"),
            file_size=data.get("file_size"),
        )


@dataclass(slots=True)
class Video:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Video:
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            width=data["width"],
            height=data["height"],
            duration=data["duration"],
            file_name=data.get("file_name"),
            mime_type=data.get("mime_type"),
            file_size=data.get("file_size"),
        )


@dataclass(slots=True)
class Voice:
    file_id: str
    file_unique_id: str
    duration: int
    mime_type: str | None = None
    file_size: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Voice:
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            duration=data["duration"],
            mime_type=data.get("mime_type"),
            file_size=data.get("file_size"),
        )


@dataclass(slots=True)
class Sticker:
    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool = False
    is_video: bool = False
    emoji: str | None = None
    file_size: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Sticker:
        return cls(
            file_id=data["file_id"],
            file_unique_id=data["file_unique_id"],
            width=data["width"],
            height=data["height"],
            is_animated=data.get("is_animated", False),
            is_video=data.get("is_video", False),
            emoji=data.get("emoji"),
            file_size=data.get("file_size"),
        )


class Message:
    __slots__ = (
        "message_id", "date", "chat", "from_user",
        "text", "photo", "document", "audio", "video",
        "voice", "sticker", "caption", "reply_to_message",
        "forward_from", "forward_date", "reply_markup", "poll",
        "location", "venue", "successful_payment", "_bot",
    )

    def __init__(
        self,
        message_id: int,
        date: int,
        chat: Chat,
        from_user: User | None,
        text: str | None,
        photo: list[PhotoSize] | None,
        document: Document | None,
        audio: Audio | None,
        video: Video | None,
        voice: Voice | None,
        sticker: Sticker | None,
        caption: str | None,
        reply_to_message: Message | None,
        forward_from: User | None,
        forward_date: int | None,
        bot: Bot,
        reply_markup: dict | None = None,
        poll: Poll | None = None,
        location: Location | None = None,
        venue: Venue | None = None,
        successful_payment: SuccessfulPayment | None = None,
    ) -> None:
        self.message_id = message_id
        self.date = date
        self.chat = chat
        self.from_user = from_user
        self.text = text
        self.photo = photo
        self.document = document
        self.audio = audio
        self.video = video
        self.voice = voice
        self.sticker = sticker
        self.caption = caption
        self.reply_to_message = reply_to_message
        self.forward_from = forward_from
        self.forward_date = forward_date
        self.reply_markup = reply_markup
        self.poll = poll
        self.location = location
        self.venue = venue
        self.successful_payment = successful_payment
        self._bot = bot

    @property
    def content(self) -> str | None:
        return self.text or self.caption

    def reply(
        self,
        text: str,
        *,
        keyboard: Inline | Reply | RemoveKeyboard | None = None,
        parse_mode: str | None = _SENTINEL,
        disable_preview: bool = False,
    ) -> Message:
        if len(text) > MAX_MESSAGE_LENGTH:
            raise MessageError(f"Текст превышает {MAX_MESSAGE_LENGTH} символов.")
        return self._bot.send_message(
            chat_id=self.chat.id,
            text=text,
            reply_to_message_id=self.message_id,
            keyboard=keyboard,
            parse_mode=parse_mode,
            disable_preview=disable_preview,
        )

    def answer(
        self,
        text: str,
        *,
        keyboard: Inline | Reply | RemoveKeyboard | None = None,
        parse_mode: str | None = _SENTINEL,
        disable_preview: bool = False,
    ) -> Message:
        if len(text) > MAX_MESSAGE_LENGTH:
            raise MessageError(f"Текст превышает {MAX_MESSAGE_LENGTH} символов.")
        return self._bot.send_message(
            chat_id=self.chat.id,
            text=text,
            keyboard=keyboard,
            parse_mode=parse_mode,
            disable_preview=disable_preview,
        )

    def edit(
        self,
        text: str,
        *,
        keyboard: Inline | None = None,
        parse_mode: str | None = _SENTINEL,
    ) -> Message:
        return self._bot.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.message_id,
            text=text,
            keyboard=keyboard,
            parse_mode=parse_mode,
        )

    def delete(self) -> bool:
        return self._bot.delete_message(chat_id=self.chat.id, message_id=self.message_id)

    def pin(self, *, disable_notification: bool = False) -> bool:
        return self._bot.pin_chat_message(
            chat_id=self.chat.id,
            message_id=self.message_id,
            disable_notification=disable_notification,
        )

    def forward(self, to_chat_id: int | str) -> Message:
        return self._bot.forward_message(
            chat_id=to_chat_id,
            from_chat_id=self.chat.id,
            message_id=self.message_id,
        )

    def copy(self, to_chat_id: int | str, *, caption: str | None = None) -> int:
        return self._bot.copy_message(
            chat_id=to_chat_id,
            from_chat_id=self.chat.id,
            message_id=self.message_id,
            caption=caption,
        )

    def reply_photo(
        self,
        photo: str,
        *,
        caption: str | None = None,
        keyboard: Inline | Reply | None = None,
        parse_mode: str | None = _SENTINEL,
    ) -> Message:
        if caption and len(caption) > MAX_CAPTION_LENGTH:
            raise MessageError(f"Подпись превышает {MAX_CAPTION_LENGTH} символов.")
        return self._bot.send_photo(
            chat_id=self.chat.id,
            photo=photo,
            caption=caption,
            keyboard=keyboard,
            parse_mode=parse_mode,
        )

    def reply_document(
        self,
        document: str,
        *,
        caption: str | None = None,
        keyboard: Inline | Reply | None = None,
    ) -> Message:
        return self._bot.send_document(
            chat_id=self.chat.id,
            document=document,
            caption=caption,
            keyboard=keyboard,
        )

    def reply_video(
        self,
        video: str,
        *,
        caption: str | None = None,
        keyboard: Inline | Reply | None = None,
        parse_mode: str | None = _SENTINEL,
    ) -> Message:
        return self._bot.send_video(
            chat_id=self.chat.id,
            video=video,
            caption=caption,
            keyboard=keyboard,
            parse_mode=parse_mode,
        )

    def reply_audio(
        self,
        audio: str,
        *,
        caption: str | None = None,
        keyboard: Inline | Reply | None = None,
    ) -> Message:
        return self._bot.send_audio(
            chat_id=self.chat.id,
            audio=audio,
            caption=caption,
            keyboard=keyboard,
        )

    def reply_voice(self, voice: str, *, caption: str | None = None) -> Message:
        return self._bot.send_voice(
            chat_id=self.chat.id,
            voice=voice,
            caption=caption,
        )

    def react(self, emoji: str) -> bool:
        return self._bot.set_message_reaction(
            chat_id=self.chat.id,
            message_id=self.message_id,
            reaction=emoji,
        )

    @classmethod
    def from_dict(cls, data: dict, bot: Bot) -> Message:
        photo = (
            [PhotoSize.from_dict(p) for p in data["photo"]] if "photo" in data else None
        )
        reply = (
            Message.from_dict(data["reply_to_message"], bot)
            if "reply_to_message" in data
            else None
        )
        return cls(
            message_id=data["message_id"],
            date=data["date"],
            chat=Chat.from_dict(data["chat"]),
            from_user=User.from_dict(data["from"]) if "from" in data else None,
            text=data.get("text"),
            photo=photo,
            document=Document.from_dict(data["document"]) if "document" in data else None,
            audio=Audio.from_dict(data["audio"]) if "audio" in data else None,
            video=Video.from_dict(data["video"]) if "video" in data else None,
            voice=Voice.from_dict(data["voice"]) if "voice" in data else None,
            sticker=Sticker.from_dict(data["sticker"]) if "sticker" in data else None,
            caption=data.get("caption"),
            reply_to_message=reply,
            forward_from=User.from_dict(data["forward_from"]) if "forward_from" in data else None,
            forward_date=data.get("forward_date"),
            bot=bot,
            reply_markup=data.get("reply_markup"),
            poll=Poll.from_dict(data["poll"]) if "poll" in data else None,
            location=Location.from_dict(data["location"]) if "location" in data else None,
            venue=Venue.from_dict(data["venue"]) if "venue" in data else None,
            successful_payment=SuccessfulPayment.from_dict(data["successful_payment"]) if "successful_payment" in data else None,
        )
