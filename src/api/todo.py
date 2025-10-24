from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app import database
from crud import todo, tag
from schemas.schema import CreateTodoSchema, TodoSchema, UpdateTodoSchema

router = APIRouter()


@router.get("/", response_model=list[TodoSchema])
def read(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 100):
    """
    Retrieve todos.
    """

    todos = todo.get(db=db, skip=skip, limit=limit)
    return todos


@router.get("/{todo_id}", response_model=TodoSchema)
def read_by_id(todo_id: int, db: Session = Depends(database.get_db)):
    todo_model = todo.get_by_id(db, todo_id)
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    return TodoSchema.model_validate(todo_model)


@router.post("/", response_model=TodoSchema)
def create(todo_schema: CreateTodoSchema, db: Session = Depends(database.get_db)):
    todo_model = todo.create(db, todo_schema)
    return TodoSchema.model_validate(todo_model)


@router.put("/{todo_id}")
def update(
    todo_id: int, todo_schema: UpdateTodoSchema, db: Session = Depends(database.get_db)
):
    todo_model = todo.update(db, todo_id, todo_schema)
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(database.get_db)):
    todo.delete(db, todo_id)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/{todo_id}/tags/{tag_id}",
    response_model=TodoSchema, # ★ 既存の `TodoSchema` に合わせました
    summary="ToDoにタグを紐付ける",
    description="指定されたtodo_idのToDoに、指定されたtag_idのタグを紐付けます。",
)
def add_tag_to_todo_endpoint(
    todo_id: int,
    tag_id: int,
    db: Session = Depends(database.get_db), # ★ 既存の `database.get_db` に合わせました
):
    """
    ToDoにタグを紐付けるためのAPIエンドポイント。
    """
    
    # 1. まず、紐付け対象のTodoが存在するかを確認
    db_todo = todo.get_by_id(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # 2. 次に、紐付けたいTagが存在するかを確認 (crud.tag を使う)
    db_tag = tag.get_by_id(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    # 3. crud の add_tag_to_todo 関数を呼び出す
    updated_todo = todo.add_tag_to_todo(db=db, todo=db_todo, tag=db_tag)
    
    # 4. 紐付けが完了した最新のTodoオブジェクトを返す
    # (crud.add_tag_to_todo が get_by_id を呼び出して返しているので、
    #  スキーマの from_attributes=True が有効なら、これで正しく変換されます)
    return updated_todo
