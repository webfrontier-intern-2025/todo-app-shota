from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app import database
from crud import todo, tag
from schemas.schema import CreateTodoSchema, TodoSchema, UpdateTodoSchema, TagSchema

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


@router.put("/{todo_id}", response_model=TodoSchema)
def update(
    todo_id: int, todo_schema: UpdateTodoSchema, db: Session = Depends(database.get_db)
):
    todo_model = todo.update(db, todo_id, todo_schema)
    if not todo_model:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_model


@router.delete("/{todo_id}")
def delete(todo_id: int, db: Session = Depends(database.get_db)):
    todo.delete(db, todo_id)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/{todo_id}/tags/{tag_id}",
    response_model=TodoSchema,
    summary="ToDoにタグを紐付ける",
    description="指定されたtodo_idのToDoに、指定されたtag_idのタグを紐付けます。",
)

@router.delete("/{todo_id}/tags/{tag_id}", response_model=TodoSchema)
def remove_tag_from_todo_endpoint(
    todo_id: int,
    tag_id: int,
    db: Session = Depends(database.get_db),
):
    updated_todo = todo.remove_tag_from_todo(db=db, todo_id=todo_id, tag_id=tag_id)
    if updated_todo is None:
        raise HTTPException(status_code=404, detail="TodoまたはTagが見つかりません")
    
    return updated_todo



def add_tag_to_todo_endpoint(
    todo_id: int,
    tag_id: int,
    db: Session = Depends(database.get_db),
):
    """
    ToDoにタグを紐付けるためのAPIエンドポイント。
    """
    
    db_todo = todo.get_by_id(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    db_tag = tag.get_by_id(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")

    updated_todo = todo.add_tag_to_todo(db=db, todo=db_todo, tag=db_tag)

    return updated_todo
