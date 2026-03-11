from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class User:
    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool = False

    @property
    def full_name(self) -> str:
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def mention(self) -> str:
        if self.username:
            return f"@{self.username}"
        return f'<a href="tg://user?id={self.id}">{self.full_name}</a>'

    @classmethod
    def from_dict(cls, data: dict) -> User:
        return cls(
            id=data["id"],
            is_bot=data.get("is_bot", False),
            first_name=data["first_name"],
            last_name=data.get("last_name"),
            username=data.get("username"),
            language_code=data.get("language_code"),
            is_premium=data.get("is_premium", False),
        )
