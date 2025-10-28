from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from models.todo import TodoModel
from models.tag import Tag
from schemas.schema import CreateTodoSchema, UpdateTodoSchema, TagSchema


def create(db: Session, create_todo_schema: CreateTodoSchema) -> TodoModel:
    todo_model = TodoModel(**create_todo_schema.model_dump(exclude_unset=True))
    db.add(todo_model)
    db.commit()
    # db.refresh(todo_model)
    return get_by_id(db, todo_model.id)


def get_by_id(db: Session, todo_id: int) -> TodoModel | None:
    return (
        db.query(TodoModel)
        .options(joinedload(TodoModel.tags))
        .filter(TodoModel.id == todo_id)
        .first()
    )


def get(db: Session, skip: int = 0, limit: int = 100) -> list[TodoModel]:
    return (
        db.query(TodoModel)
        .options(joinedload(TodoModel.tags))
        .order_by(TodoModel.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


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


def remove_tag_from_todo(db: Session, todo_id: int, tag_id: int) -> Optional[TodoModel]:
    """
    指定されたToDoから指定されたTagの紐付けを解除する。
    中間テーブル (todo_tags) から対応する行を削除する。

    Args:
        db (Session): SQLAlchemyデータベースセッション。
        todo_id (int): 対象となるToDoのID。
        tag_id (int): 削除するTagのID。

    Returns:
        Optional[TodoModel]: 更新後のToDoオブジェクト。ToDoまたはTagが見つからない場合はNone。
    """
    todo_item = get_by_id(db, todo_id)
    if not todo_item:
        print(f"ToDo not found with id: {todo_id}")
        return None

  
    tag_item = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag_item:
        print(f"Tag not found with id: {tag_id}")
        return None

    if tag_item in todo_item.tags:
        print(f"Removing tag {tag_id} ({tag_item.name}) from todo {todo_id} ({todo_item.content})") # ログ出力
        todo_item.tags.remove(tag_item)
        db.add(todo_item) 
        db.commit()      
        print("Commit successful.")
    else:
        print(f"Tag {tag_id} ({tag_item.name}) is not associated with todo {todo_id} ({todo_item.content}). No action taken.")
        pass

    return get_by_id(db, todo_id)


def add_tag_to_todo(db: Session, todo: TodoModel, tag: Tag) -> Optional[TodoModel]:
    """
    指定されたIDのTodoに、指定されたIDのTagを紐づけます。
    """

    if tag not in todo.tags:
        todo.tags.append(tag)

        db.add(todo)
        db.commit()
        # db.refresh(todo)

    return get_by_id(db, todo.id)
