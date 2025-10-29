from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass


class TagRead(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime


    todos: List["TodoRead"] = []

    model_config = ConfigDict(
        from_attributes=True
    )

from .todo import TodoRead

TagRead.model_rebuild()
