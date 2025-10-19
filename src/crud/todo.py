from sqlalchemy.orm import Session

from models.todo import TodoModel
from schemas.schema import CreateTodoSchema, UpdateTodoSchema


def create(db: Session, create_todo_schema: CreateTodoSchema) -> TodoModel:
    todo_model = TodoModel(**create_todo_schema.model_dump(exclude_unset=True))
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


def get_by_id(db: Session, todo_id: int) -> TodoModel | None:
    return db.query(TodoModel).filter(TodoModel.id == todo_id).first()


def get(db: Session, skip: int = 0, limit: int = 100) -> list[TodoModel]:
    return db.query(TodoModel).offset(skip).limit(limit).all()


def update(
    db: Session, todo_model_id: int, update_todo_schema: UpdateTodoSchema
) -> TodoModel | None:
    todo_model = db.query(TodoModel).filter(TodoModel.id == todo_model_id).first()
    if todo_model is None:
        return todo_model

    update_todo_schema_obj = update_todo_schema.model_dump(exclude_unset=True)
    for key, value in update_todo_schema_obj.items():
        setattr(todo_model, key, value)
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return todo_model


def delete(db: Session, todo_model_id: int) -> int | None:
    todo_model = db.query(TodoModel).get(todo_model_id)
    if todo_model is None:
        return None
    db.delete(todo_model)
    db.commit()
    return todo_model_id
