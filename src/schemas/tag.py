from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# ( 'TodoRead' を循環参照するため、 'TodoRead' の定義を先に読み込ませるトリック)
# このファイルでは 'Todo' スキーマはまだ定義されていないので、
# まずは 'Todo' という名前のプレースホルダー（仮の姿）を定義します。


# --- Tagの基本スキーマ ---
class TagBase(BaseModel):
    name: str

# Tagを作成するときのスキーマ (POST /v1/tag/ の入力用)
class TagCreate(TagBase):
    pass

# Tagを読み取るときのスキーマ (GET /v1/tag/ や POST /v1/tag/ の出力用)
class TagRead(TagBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
        # ★★★ ここを修正 ★★★
    # プレースホルダーの `Todo` ではなく、
    # 最終的にインポートする `TodoRead` クラスの「名前（文字列）」を
    # List["TodoRead"] のように指定します。
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
