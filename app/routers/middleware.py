from fastapi import HTTPException, Request

# オリジナルのクラスをインポート
from config.config import Config
from ..services.app_setting import AppSetting


# ミドルウェアの設定を行うためのクラス
class Middleware:
    # リクエストのボディサイズを検証するため、ミドルウェアを設定する
    @classmethod
    async def validate_content_length(cls, request: Request, call_next: any) -> any:
        # リクエストのボディサイズを検証し、サイズが大きすぎる場合は413エラーを発生する
        try:
            AppSetting.validate_content_length(request, Config.max_content_length)
        except HTTPException as ex:
            print(ex)
            raise ex

        # 検証に問題がなければ、次の処理を実行する
        return await call_next(request)
