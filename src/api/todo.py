from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import database
from crud import todo
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
