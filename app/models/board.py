from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from .base import Base

class Board(Base):
    __tablename__ = "board"

    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    owner: Mapped[str] = mapped_column(String)
    cards: Mapped[List["Card"]] = relationship(back_populates="board")