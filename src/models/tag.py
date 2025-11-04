from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, TIMESTAMP

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

# 上記にtimestampのimportを移動
# from sqlalchemy.types import TIMESTAMP

from app.database import Base

from models.todo_tag import todo_tag_association_table


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    # 発表の時点でタグの一意制約は実装済み
    name: Mapped[str] = mapped_column(
        String(30), unique=True, index=True, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    todos: Mapped[List["TodoModel"]] = relationship(
        "TodoModel", secondary=todo_tag_association_table, back_populates="tags"
    )
