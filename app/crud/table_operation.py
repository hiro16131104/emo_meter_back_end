# オリジナルのクラスをインポート
from ..models.dynamodb_models import UserModel


# テーブルを操作するためのクラス
class TableOperation:
    # ユーザーテーブルが存在するか確認する（存在する場合はTrueを返す）
    @classmethod
    def exist_user_table(cls) -> bool:
        return UserModel.exists()

    # ユーザーテーブルを作成する
    @classmethod
    def create_user_table(cls):
        # 1秒間に1KB以下のデータ書き込み/読み込みができるように設定する
        UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    # ユーザーテーブルを削除する
    @classmethod
    def delete_user_table(cls):
        UserModel.delete_table()
