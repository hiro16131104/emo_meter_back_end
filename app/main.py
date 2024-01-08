from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException

# オリジナルのクラスをインポート
from .services.app_setting import AppSetting
from .routers import api
from .routers.middleware import Middleware
from .routers.exception_handler import ExceptionHandler


# 共通変数の定義
app = FastAPI()

# アプリの初期設定
AppSetting.allow_cors(app)
# ミドルウェアを設定する
app.middleware("http")(Middleware.validate_content_length)
# エラーハンドラーを設定する
app.exception_handler(StarletteHTTPException)(ExceptionHandler.http_exception_handler)
app.exception_handler(Exception)(ExceptionHandler.exception_handler)
# ルーター（エンドポイント）を登録する
app.include_router(api.router)


# 接続テスト用のエンドポイント（GET）
@app.get("/")
def test_get() -> str:
    return "接続テストOK。このURLは有効です。"
