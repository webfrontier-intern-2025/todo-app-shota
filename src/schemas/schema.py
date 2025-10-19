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

