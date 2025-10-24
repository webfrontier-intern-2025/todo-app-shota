from datetime import datetime, date
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --------------------------------
# Tag スキーマ
# --------------------------------


class TagBase(BaseModel):
    name: str


class CreateTagSchema(TagBase):
    pass


class UpdateTagSchema(TagBase):
    name: Optional[str] = None


# ★★★ 新規追加 ★★★
# 「Todoのレスポンス」に含めるための、
# `todos` リストを持たないシンプルなTagスキーマ
class TagForTodoResponse(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --------------------------------
# Todo スキーマ
# --------------------------------


class TodoBase(BaseModel):
    content: str
    deadline: Optional[date] = None


class CreateTodoSchema(TodoBase):
    pass


class UpdateTodoSchema(BaseModel):
    content: Optional[str] = None
    deadline: Optional[date] = None
    completed: Optional[bool] = None


# ★★★ 新規追加 ★★★
# 「Tagのレスポンス」に含めるための、
# `tags` リストを持たないシンプルなTodoスキーマ
class TodoForTagResponse(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --------------------------------
# フルレスポンス用スキーマ
# --------------------------------


# Tagのフルレスポンス用スキーマ
# (循環参照を防ぐため、`TodoForTagResponse` を使う)
class TagSchema(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime

    # ★★★ 修正点 ★★★
    # `List["TodoSchema"]` から `List[TodoForTagResponse]` に変更
    todos: List[TodoForTagResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Todoのフルレスポンス用スキーマ
# (循環参照を防ぐため、`TagForTodoResponse` を使う)
class TodoSchema(TodoBase):
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime

    # ★★★ 修正点 ★★★
    # `List["TagSchema"]` から `List[TagForTodoResponse]` に変更
    tags: List[TagForTodoResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- 循環参照の解決 ---
# `model_rebuild()` は、文字列（前方参照）を使っていないので、
# もはや不要です。削除しても問題ありません。
# TodoSchema.model_rebuild()
# TagSchema.model_rebuild()
