from datetime import datetime, date
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class TodoBase(BaseModel):
    content: str
    deadline: Optional[date] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    content: Optional[str] = None
    deadline: Optional[date] = None
    completed: Optional[bool] = None


class TodoRead(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime


    tags: List["TagRead"] = []

    model_config = ConfigDict(
        from_attributes=True
    )


from .tag import TagRead

TodoRead.model_rebuild()
