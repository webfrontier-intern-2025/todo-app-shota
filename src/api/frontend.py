from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from fastapi import Request

from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app import database
from app.templating import templates  # ★ 1. 新しい設定ファイルからインポート
from crud import todo


# このルーターはHTMLページを返すためだけのものです
router = APIRouter(
    tags=["Frontend"],  # /docs で "Frontend" としてグループ化されます
    default_response_class=HTMLResponse,  # デフォルトのレスポンスをHTMLに設定
)


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(database.get_db)):
    """
    トップページ（ToDo一覧）を表示します。
    """
    # 1. データベースから全てのToDoを取得する
    #    crud.todo.get は joinedload(TodoModel.tags) を使っているので、
    #    タグ情報も一緒に取得されます。
    todos = todo.get(db=db, skip=0, limit=100)

    # 2. テンプレートにデータを渡してHTMLを生成する
    return templates.TemplateResponse(
        "index.html",  # templates/index.html を使用
        {
            "request": request,
            "todos": todos,  # ★ 取得したToDoのリストをテンプレートに渡す
            "page_title": "ToDoアプリ",  # ★ タイトルも渡す
        },
    )


# ToDo作成ページ用のエンドポイント
@router.get("/todo/new", response_class=HTMLResponse)
async def create_todo_form(request: Request):
    """
    ToDo作成フォームのページを表示します。
    """
    return templates.TemplateResponse(
        "create_todo.html",  # templates/create_todo.html を使用
        {
            "request": request,
            "page_title": "新しいToDoの作成",
        },
    )


@router.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Jinja2テンプレートを使ってHTMLページを返します。
    """
    return templates.TemplateResponse(
        "index.html",  # templates/index.html ファイルを指定
        {
            "request": request,
            "page_title": "ToDoアプリのフロントエンド",  # HTML側に渡す変数
        },
    )
