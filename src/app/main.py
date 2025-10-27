import json
from logging import config
# import os

from fastapi import FastAPI
# from fastapi import Request
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse


from fastapi_route_logger_middleware import RouteLoggerMiddleware
from starlette.middleware.cors import CORSMiddleware

from app import settings
from app.router import api_router
from api import frontend

# Jinja2テンプレートの設定=>app/temlating.py

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_VER_STR}/openapi.json"
)

with open(settings.LOGGING_CONF, encoding="utf-8") as f:
    config.dictConfig(json.load(f))

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# --- ★★★ 6. テスト用HTMLページを返すエンドポイントを追加 ★★★ ---
# (APIルーター（/v1/...）より先に定義します)


# ★★★ 4. 新しいルーターを登録 ★★★
# これが / (トップページ) や /todo/new などのHTMLページを返します
app.include_router(frontend.router)

# --- ここまでが追加したエンドポイント ---

app.include_router(api_router, prefix=settings.API_VER_STR)
