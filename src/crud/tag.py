from sqlalchemy.orm import Session

from models.tag import Tag
from schemas.schema import CreateTagSchema, UpdateTagSchema


def create(db: Session, create_tag_schema: CreateTagSchema) -> Tag:
    tag_model = Tag(**create_tag_schema.model_dump(exclude_unset=True))
    db.add(tag_model)
    db.commit()
    db.refresh(tag_model)
    return tag_model


def get_by_id(db: Session, tag_id: int) -> Tag | None:
    return db.query(Tag).filter(Tag.id == tag_id).first()


def get(db: Session, skip: int = 0, limit: int = 100) -> list[Tag]:
    return db.query(Tag).offset(skip).limit(limit).all()


def update(
    db: Session, tag_model_id: int, update_tag_schema: UpdateTagSchema
) -> Tag | None:
    tag_model = db.query(Tag).filter(Tag.id == tag_model_id).first()
    if tag_model is None:
        return tag_model

    update_tag_schema_obj = update_tag_schema.model_dump(exclude_unset=True)
    for key, value in update_tag_schema_obj.items():
        setattr(tag_model, key, value)
    db.add(tag_model)
    db.commit()
    db.refresh(tag_model)
    return tag_model


def delete(db: Session, tag_model_id: int) -> int | None:
    tag_model = db.query(Tag).get(tag_model_id) # .get() は主キーでの取得
    if tag_model is None:
        return None
    db.delete(tag_model)
    db.commit()
    return tag_model_id
