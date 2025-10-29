from datetime import datetime, date
from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class TagBase(BaseModel):
    name: str


class CreateTagSchema(TagBase):
    pass


class UpdateTagSchema(TagBase):
    name: Optional[str] = None

class TagForTodoResponse(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TodoBase(BaseModel):
    content: str
    deadline: Optional[date] = None


class CreateTodoSchema(TodoBase):
    pass


class UpdateTodoSchema(BaseModel):
    content: Optional[str] = None
    deadline: Optional[date] = None
    completed: Optional[bool] = None


class TodoForTagResponse(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TagSchema(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    todos: List[TodoForTagResponse] = []

    model_config = ConfigDict(from_attributes=True)

class TodoSchema(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    tags: List[TagForTodoResponse] = []

    model_config = ConfigDict(from_attributes=True)