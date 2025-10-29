from sqlalchemy import Column, ForeignKey, Integer, Table
from app.database import Base

todo_tag_association_table = Table(
    "todo_tags",
    Base.metadata,
    Column("todo_id", Integer, ForeignKey("todo.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
