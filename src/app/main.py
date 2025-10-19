import json
from logging import config

from fastapi import FastAPI
from fastapi_route_logger_middleware import RouteLoggerMiddleware
from starlette.middleware.cors import CORSMiddleware

from app import settings
from app.router import api_router

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

app.include_router(api_router, prefix=settings.API_VER_STR)
