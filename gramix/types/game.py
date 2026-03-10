from __future__ import annotations
from dataclasses import dataclass

from gramix.types.user import User


@dataclass(slots=True)
class GameHighScore:
    position: int
    user: User
    score: int

    @classmethod
    def from_dict(cls, data: dict) -> GameHighScore:
        return cls(
            position=data["position"],
            user=User.from_dict(data["user"]),
            score=data["score"],
        )
