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



# --- 循環参照の解決 ---
# 'TagRead' の完全な定義をインポートします
from .tag import TagRead

# 'TodoRead' スキーマが参照していた 'Tag' プレースホルダーを、
# 'TagRead' の完全な定義で更新します。
TodoRead.model_rebuild()
