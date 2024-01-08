import string
import random
from datetime import datetime


# インスタンス化せずに使用できるメソッドを集約したクラス
class Utility:
    # 指定した桁数のランダムな文字列を生成する
    @classmethod
    def generate_random_string(cls, length) -> str:
        # 英字（大文字・小文字）と数字を結合した文字列を生成する
        letters_and_digits: str = string.ascii_letters + string.digits
        result = ""

        # 指定した桁数分のランダムな文字を追加する
        for _ in range(length):
            result += random.choice(letters_and_digits)

        return result

    # "yyyy-mm-dd"形式で日付を取得する
    @classmethod
    def get_date_str(cls) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    # 文字列から複数の文字を除去する
    @classmethod
    def remove_chars(self, text: str, chars: list[str]) -> str:
        result_text = text

        # 引数で指定した文字を1つずつ除去する
        for char in chars:
            result_text = result_text.replace(char, "")

        return result_text
