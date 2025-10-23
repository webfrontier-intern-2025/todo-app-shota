from fastapi import APIRouter

from api import todo
from api import tag

api_router = APIRouter()

api_router.include_router(todo.router, prefix="/todo", tags=["todo"])
api_router.include_router(tag.router, prefix="/tag", tags=["tag"])
