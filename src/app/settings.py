import os
from os.path import dirname, join

from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

PROJECT_NAME = os.environ.get("PROJECT_NAME") or ""

# DATABASE_URL = os.environ.get("DATABASE_URL") or ""
DATABASE_URL = "sqlite:///./todo.db"

API_VER_STR = os.environ.get("API_VER_STR") or ""
BACKEND_CORS_ORIGINS = os.environ.get("BACKEND_CORS_ORIGINS") or ""
LOGGING_CONF = os.environ.get("LOGGING_CONF") or ""
