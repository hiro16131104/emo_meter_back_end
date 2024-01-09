from datetime import datetime

# オリジナルのクラスをインポート
from ..models.dynamodb_models import UserModel


# ユーザーテーブルを操作するためのクラス
class UserOperation:
    # レコードを作成する
    @classmethod
    def create_user(cls, user_id: str) -> None:
        # レコード（ユーザーID、作成日時、最終アクセス日時）を作成する
        user = UserModel(user_id=user_id)
        user.save()

    # レコードを取得する
    @classmethod
    def read_user(cls, user_id: str) -> UserModel | None:
        # ユーザーIDをキーとして検索し、最初のレコードを取得する（検索結果がなければNoneを返す）
        user: UserModel = next(UserModel.query(user_id), None)
        return user

    # 全てのレコードを取得する（'last_accessed_at'の降順）
    @classmethod
    def read_all_users(cls) -> list[UserModel]:
        # 全てのレコードを取得する
        users: list[UserModel] = list(UserModel.scan())

        # 'last_accessed_at'の降順にソートする
        users.sort(key=lambda x: x.last_accessed_at, reverse=True)
        return users

    # レコード件数を取得する
    @classmethod
    def read_user_count(cls) -> int:
        # 全てのレコードを取得する
        users: list[UserModel] = list(UserModel.scan())
        # ユーザーテーブルのレコード件数を返却する
        return len(users)

    # レコードを更新する
    @classmethod
    def update_user(cls, user_id: str, last_accessed_at: datetime = None) -> None:
        # ユーザーIDをキーにレコードを取得する
        user: UserModel = cls.read_user(user_id)
        # 最終アクセス日時を更新する
        user.last_accessed_at = last_accessed_at or datetime.now()
        user.save()

    # レコードを削除する
    @classmethod
    def delete_user(cls, user_id: str) -> None:
        # ユーザーIDをキーにレコードを取得する
        user: UserModel = cls.read_user(user_id)
        # レコードを削除する
        user.delete()
