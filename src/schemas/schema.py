from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TodoSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    completed: bool | None = None
    deadline: datetime | None = None

class TodoSchema(TodoSchemaBase):
    id: int
    content: str


class CreateTodoSchema(TodoSchemaBase):
    content: str


class UpdateTodoSchema(TodoSchemaBase):
    content: str | None = None

class TagSchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class TagSchema(TagSchemaBase):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

class CreateTagSchema(TagSchemaBase):
    name: str

class UpdateTagSchema(TagSchemaBase):
    name: str | None = None


