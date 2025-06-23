from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Board(Base):
    __tablename__ = "board"

    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    cards: Mapped[list["Card"]] = relationship(back_populates="board")