from datetime import datetime, date

# Fieldのimportを追加
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional


class TagBase(BaseModel):
    # ↓ バリデーションを適用 (1文字以上30文字以下)
    name: str = Field(..., min_length=1, max_length=30)


class CreateTagSchema(TagBase):
    pass


class UpdateTagSchema(TagBase):
    # ↓ 更新時もバリデーションが効くようにする
    name: Optional[str] = Field(None, min_length=1, max_length=30)


class TagForTodoResponse(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TodoBase(BaseModel):
    # ↓ バリデーションを適用する (1文字以上30文字以下)
    content: str = Field(..., min_length=1, max_length=30)
    deadline: Optional[date] = None


class CreateTodoSchema(TodoBase):
    pass


class UpdateTodoSchema(BaseModel):
    # ↓ 更新時もバリデーションが効くようにする
    content: Optional[str] = Field(None, min_length=1, max_length=30)
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
