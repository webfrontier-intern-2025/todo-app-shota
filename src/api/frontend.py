from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse

from fastapi import Request

from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app import database
from app.templating import templates
from crud import todo

from app.database import get_db

router = APIRouter(
    tags=["Frontend"],
    default_response_class=HTMLResponse,
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(database.get_db)):

    todos = todo.get(db=db, skip=0, limit=100)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "todos": todos,
            "page_title": "ToDoアプリ",
        },
    )

@router.get("/todo/new", response_class=HTMLResponse)
async def create_todo_form(request: Request):

    return templates.TemplateResponse(
        "create_todo.html",
        {
            "request": request,
            "page_title": "新しいToDoの作成",
        },
    )

@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_title": "ToDoアプリのフロントエンド",
        },
    )

@router.get("/todo/{todo_id}/edit", response_class=HTMLResponse)
async def show_edit_todo_form(request: Request, todo_id: int, db: Session = Depends(get_db)):

    todo_item = todo.get_by_id(db, todo_id=todo_id)

    if todo_item is None:
        raise HTTPException(status_code=404, detail="指定されたToDoが見つかりません。")

    return templates.TemplateResponse(
        "edit_todo.html",
        {
            "request": request,
            "page_title": f"ToDoの編集 (ID: {todo_id})",
            "todo": todo_item
        }
    )

@router.get("/licenses", response_class=HTMLResponse)
async def show_licenses_page(request: Request):

    return templates.TemplateResponse(
        "licenses.html",
        {
            "request": request,
            "page_title": "ライセンスについて",
        },
    )