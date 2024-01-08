from app.services.file_access import FileAccess


# 設定ファイルの内容を格納するためのクラス
class Config:
    # クラス変数の定義
    config: dict = FileAccess("./config/settings.json").read_json_file()
    config_secret: dict = FileAccess("./config/secrets.json").read_json_file()
    environment: str = config["environment"]["value"]
    server: dict = config["server"][environment]
    database: dict = config["database"][environment]
    max_content_length: int = config["limit"]["maxContentLength"]
    model_name: str = config["learnedModel"]["semanticSearch"]
    max_word_count: int = config["similarity"]["maxWordCount"]
    minimum_similarity: float = config["similarKeyword"]["minimumSimilarity"]
    password_admin: dict = config_secret["password"]["admin"]
