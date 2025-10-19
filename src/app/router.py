from fastapi import APIRouter

from api import todo

api_router = APIRouter()

api_router.include_router(todo.router, prefix="/todo", tags=["todo"])
