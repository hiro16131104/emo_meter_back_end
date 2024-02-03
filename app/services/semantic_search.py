from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from torch import Tensor


# 文とキーワードの類似度を計算するためのクラス
class SemanticSearch:
    # メモリを節約するため、クラス変数として定義する
    # 文章を格納するためのリスト
    sentences: list[str] = []
    # 学習済みモデルを格納するための変数
    learned_model: SentenceTransformer = None

    def __init__(self, keyword: str) -> None:
        self.keyword = keyword
        # 類似度を格納するためのリスト（'sentences'の要素番号と対応する）
        self.similarities: list[float] = []

        if not self.sentences:
            raise ValueError(
                "クラス変数'sentences'が空です。先にset_sentences()を実行してください。"
            )
        elif not self.learned_model:
            raise ValueError(
                "クラス変数'learned_model'が空です。先にset_learned_model()を実行してください。"
            )

    # クラス変数'sentences'に文章を格納する
    @classmethod
    def set_sentences(cls, sentences: list[str]) -> None:
        cls.sentences = sentences

    # クラス変数'learned_model'に学習済みモデルを格納する
    @classmethod
    def set_learned_model(cls, model_name: str) -> None:
        # 学習済みモデルが未定義の場合のみ、学習済みモデルを読み込む
        if not cls.learned_model:
            cls.learned_model = SentenceTransformer(model_name)

    # 文章とキーワードの類似度を計算する
    def calculate_similarity(self) -> None:
        # キーワードをベクトル化する
        keyword_embedding: Tensor = self.learned_model.encode(
            self.keyword, convert_to_tensor=True
        )
        self.similarities = []

        # 文章のベクトルとキーワードのベクトルの類似度を計算する
        for sentence in self.sentences:
            # 文章をベクトル化する
            sentence_embedding: Tensor = self.learned_model.encode(
                sentence, convert_to_tensor=True
            )
            # コサイン類似度を計算する
            similarity: Tensor = cos_sim(keyword_embedding, sentence_embedding)

            # 類似度を少数に変換して、リストに格納する（1に近いほど類似度が高い）
            self.similarities.append(round(float(similarity), 4))
