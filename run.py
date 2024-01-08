import uvicorn

# オリジナルのクラスをインポート
from config.config import Config


# スクリプトが直接実行された場合の処理
if __name__ == "__main__":
    # サーバーを起動する
    uvicorn.run(
        "app.main:app",
        host=Config.server["host"],
        port=Config.server["port"],
        reload=Config.server["reload"],
        log_level=Config.server["logLevel"],
    )
