from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute
from datetime import datetime

# オリジナルのクラスをインポート
from config.config import Config


# ユーザーテーブルのモデルを定義するためのクラス
class UserModel(Model):
    # テーブルの基本情報
    class Meta:
        table_name = Config.database["tableName"]["user"]
        # 東京リージョン
        region = Config.database["region"]
        # host = "http://localhost:5050"

    # 列の定義
    # ユーザーID（str）
    user_id = UnicodeAttribute(hash_key=True, null=False)
    # 作成日時（datetime）
    created_at = UTCDateTimeAttribute(range_key=True, default=datetime.now, null=False)
    # 最終アクセス日時（datetime）
    last_accessed_at = UTCDateTimeAttribute(default=datetime.now, null=False)
