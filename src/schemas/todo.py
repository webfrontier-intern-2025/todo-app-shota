from datetime import datetime, date
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Tagのプレースホルダーを先に定義 ---



# --- Todoの基本スキーマ ---
class TodoBase(BaseModel):
    content: str
    deadline: Optional[date] = None

# Todoを作成するときのスキーマ
class TodoCreate(TodoBase):
    pass

# Todoを更新するときのスキーマ
class TodoUpdate(BaseModel):
    content: Optional[str] = None
    deadline: Optional[date] = None
    completed: Optional[bool] = None

# Todoを読み取るときのスキーマ (レスポンス用)
class TodoRead(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    # ★★★ ここが重要 ★★★
    # このTodoに関連するTagのリストを含める
    tags: List["TagRead"] = []

    model_config = ConfigDict(
        from_attributes=True  # SQLAlchemyモデルからPydanticモデルへ変換
    )



# --- 循環参照の解決 ---
# 'TagRead' の完全な定義をインポートします
from .tag import TagRead

# 'TodoRead' スキーマが参照していた 'Tag' プレースホルダーを、
# 'TagRead' の完全な定義で更新します。
TodoRead.model_rebuild()
