import os

from fastapi.templating import Jinja2Templates

# --- ★★★ 5. Jinja2テンプレートエンジンの設定 ★★★ ---

# このファイル(main.py)の場所を基準に、
# プロジェクトのルートディレクトリ（`src` の親）を特定します
# (.../practical-fastapi/src/app/main.py -> .../practical-fastapi/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# `templates` ディレクトリのパスを指定します
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# FastAPIにJinja2テンプレートの場所を教えます
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# --- ここまでがJinja2の設定 ---