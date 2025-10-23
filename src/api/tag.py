from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import database
from crud import tag
from schemas.schema import CreateTagSchema, TagSchema, UpdateTagSchema

router = APIRouter()


@router.get("/", response_model=list[TagSchema])
def read(db: Session = Depends(database.get_db), skip: int = 0, limit: int = 100):
    """
    Retrieve tags.
    """

    tags = tag.get(db=db, skip=skip, limit=limit)
    return tags


@router.get("/{tag_id}", response_model=TagSchema)
def read_by_id(tag_id: int, db: Session = Depends(database.get_db)):
    tag_model = tag.get_by_id(db, tag_id)
    if not tag_model:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagSchema.model_validate(tag_model)


@router.post("/", response_model=TagSchema)
def create(tag_schema: CreateTagSchema, db: Session = Depends(database.get_db)):
    tag_model = tag.create(db, tag_schema)
    return TagSchema.model_validate(tag_model)


@router.put("/{tag_id}")
def update(
    tag_id: int, tag_schema: UpdateTagSchema, db: Session = Depends(database.get_db)
):
    tag_model = tag.update(db, tag_id, tag_schema)
    if not tag_model:
        raise HTTPException(status_code=404, detail="Tag not found")
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/{tag_id}")
def delete(tag_id: int, db: Session = Depends(database.get_db)):
    tag.delete(db, tag_id)
    return Response(status_code=status.HTTP_200_OK)
