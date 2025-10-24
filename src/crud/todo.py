from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from models.todo import TodoModel
from models.tag import Tag
from schemas.schema import CreateTodoSchema, UpdateTodoSchema


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


def add_tag_to_todo(db: Session, todo: TodoModel, tag: Tag) -> Optional[TodoModel]:
    """
    指定されたIDのTodoに、指定されたIDのTagを紐づけます。
    """

    # 1. 紐付け対象のTodoを取得 (この時点では tags は不要)
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if not todo:
        return None  # Todoが見つからない

    # 2. 紐付けたいTagを取得
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        return None  # Tagが見つからない

    # 3. すでに紐付いていないか確認 (効率化のため)
    if tag not in todo.tags:
        # 4. TodoのtagsリストにTagを追加する
        #    (SQLAlchemyが中間テーブルへのINSERTを自動で行ってくれます)
        todo.tags.append(tag)

        # 5. データベースセッションに追加してコミット
        db.add(todo)
        db.commit()
        # db.refresh(todo)

    # 6. 関連Tagが読み込まれた最新のTodoを返す
    #    (get_by_id を再利用するのが最も安全で確実です)
    return get_by_id(db, todo_id)
