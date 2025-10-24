from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import Boolean, Date, DateTime, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func


from app.database import Base

from models.todo_tag import todo_tag_association_table


class TodoModel(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    content: Mapped[str] = mapped_column(String(256), nullable=False)
    completed: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="False"
    )
    deadline: Mapped[Optional[DateTime]] = mapped_column(DateTime, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    tags: Mapped[List["Tag"]] = relationship(
        "Tag",
        secondary=todo_tag_association_table,
        back_populates="todos"
    )
