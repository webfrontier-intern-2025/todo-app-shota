from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse

from fastapi import Request

from fastapi.responses import HTMLResponse

from sqlalchemy.orm import Session

from app import database
from app.templating import templates  # ★ 1. 新しい設定ファイルからインポート
from crud import todo

from app.database import get_db


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

# ★★★ ToDo編集ページ表示用のエンドポイント (ここを追加) ★★★
@router.get("/todo/{todo_id}/edit", response_class=HTMLResponse)
async def show_edit_todo_form(request: Request, todo_id: int, db: Session = Depends(get_db)):
    """
    既存のToDoを編集するためのフォームページを表示する。
    """
    # 1. 指定されたIDのToDoをDBから取得する (crud.todo.get_by_id を使用)
    todo_item = todo.get_by_id(db, todo_id=todo_id)

    # 2. ToDoが見つからない場合は404エラーを返す
    if todo_item is None:
        raise HTTPException(status_code=404, detail="指定されたToDoが見つかりません。")

    # 3. ToDoが見つかったら、編集用テンプレートにデータを渡して表示する
    return templates.TemplateResponse(
        "edit_todo.html", # 使用するHTMLテンプレートファイル名
        {
            "request": request,
            "page_title": f"ToDoの編集 (ID: {todo_id})", # ページタイトル
            "todo": todo_item # ★★★ 取得したToDoデータを 'todo' という名前でテンプレートに渡す ★★★
        }
    )