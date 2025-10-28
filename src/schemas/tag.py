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

    # class Config:
    #     from_attributes = True 
    # ↓ Pydantic v2 の ConfigDict を使うと、より明確です
    model_config = ConfigDict(
        from_attributes=True  # SQLAlchemyモデルからPydanticモデルへ変換
    )


# --- 循環参照の解決 ---
# 'TodoRead' の完全な定義をインポートします
# (todo.py 側に 'TodoRead' が必要です)
from .todo import TodoRead

# 'TagRead' スキーマが参照していた 'Todo' プレースホルダーを、
# 'TodoRead' の完全な定義で更新します。
TagRead.model_rebuild()
