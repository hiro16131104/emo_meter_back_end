from fastapi import FastAPI, HTTPException, Request
from starlette.middleware.cors import CORSMiddleware


# FastAPIアプリの設定を行うためのクラス
class AppSetting:
    # サーバーを跨いでのリクエストを許可する
    @classmethod
    def allow_cors(cls, app: FastAPI) -> None:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # リクエストのボディサイズを検証し、サイズが大きすぎる場合はエラーを発生する
    @classmethod
    def validate_content_length(
        cls, request: Request, max_content_length: int
    ) -> HTTPException | None:
        # リクエストのボディサイズを取得する
        content_length: int = (
            int(request.headers["content-length"])
            if request.headers.get("content-length")
            else 0
        )
        # ボディサイズが最大値を超えていた場合はエラーを発生させる
        if content_length > max_content_length:
            raise HTTPException(413, "Payload too large.")
