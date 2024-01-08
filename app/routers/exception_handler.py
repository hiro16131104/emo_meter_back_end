from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


# エラー処理を行うためのクラス
class ExceptionHandler:
    # エラーが発生したとき処理
    @classmethod
    def http_exception_handler(
        cls, request: Request, ex: StarletteHTTPException
    ) -> JSONResponse:
        content: dict[str, any] = {
            "error": {"statusCode": ex.status_code, "description": ex.detail}
        }
        print(ex)
        return JSONResponse(content, ex.status_code)

    # その他のエラーが発生したとき処理
    @classmethod
    def exception_handler(cls, request: Request, ex: Exception) -> JSONResponse:
        print(ex)
        return cls.http_exception_handler(
            request, HTTPException(500, "Internal Server Error")
        )
