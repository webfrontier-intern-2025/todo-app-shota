from sqlalchemy import Column, ForeignKey, Integer, Table
from app.database import Base

# TodoModel と Tag の間の多対多関係のための
# 「中間テーブル（関連テーブル）」の定義
#
# このテーブルは単にIDのペアを保持するだけなので、
# Tag や TodoModel のような「クラス(class)」として定義する代わりに、
# このようにシンプルな `Table` オブジェクトとして定義するのが一般的

todo_tag_association_table = Table(
    "todo_tags",  # 1. データベース上のテーブル名
    Base.metadata,
    # 2. todoテーブルのidへの外部キー
    Column("todo_id", Integer, ForeignKey("todo.id"), primary_key=True),
    # 3. tagsテーブルのidへの外部キー
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)
