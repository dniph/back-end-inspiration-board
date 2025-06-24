from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .base import Base
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .board import Board

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int] = mapped_column(default=0)
    board_id: Mapped[int] = mapped_column(ForeignKey("board.board_id"))
    board: Mapped["Board"] = relationship(back_populates="cards")

    def to_dict(self):
        return {
            "id": self.card_id,
            "card_message": self.message,
            "likes": self.likes_count,
            "board_id": self.board_id
        }

    @classmethod
    def from_dict(cls, data):
        card = cls()
        card.message = data["message"]
        card.board_id = data["board_id"]
        return card