from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from ..db import db
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .card import Card

class Board(db.Model):
    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    def to_dict(self):
        return {
            "board_id": self.board_id,
            "title": self.title,
            "owner": self.owner
        }
    
    @classmethod
    def from_dict(cls, data):
        board = cls()
        board.title = data["title"]
        board.owner = data["owner"]
        return board