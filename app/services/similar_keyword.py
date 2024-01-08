# 文章と類似度の高いキーワードを判定するためのクラス
class SimilarKeyword:
    def __init__(
        self,
        sentences: list[str],
        similar_infomations: list[dict[str, str | list[float]]],
    ) -> None:
        # 文章
        self.sentences = sentences
        # キーワードと類似度のリスト
        self.similar_infomations = similar_infomations

    # 各文章に対して類似度が最も高いキーワードを決定する（'minimum_similarity'は類似度の足切り値）
    def determine_similar_keyword(
        self, minimum_similarity: float = 0.0000
    ) -> list[dict[str, str | float]]:
        results: list[dict[str, str | float]] = []

        for i in range(len(self.sentences)):
            # 文、キーワード、類似度を格納する
            result: dict[str, str | float] = {
                "sentence": self.sentences[i],
                "keyword": "",
                "similarity": minimum_similarity,
            }

            for similar_infomation in self.similar_infomations:
                # 文に対応する類似度を取得する
                similarity: float = similar_infomation["similarities"][i]

                # 今回ループ処理の類似度が前回ループ処理の類似度（又は初期値）よりも低い場合はスキップする
                if not similarity > result["similarity"]:
                    continue

                # キーワードと類似度を格納する
                result["keyword"] = similar_infomation["keyword"]
                result["similarity"] = similarity

            # 足切り値を超える類似度がない場合は類似度に0.0000を格納する
            if result["keyword"] == "":
                result["similarity"] = 0.0000

            results.append(result)

        return results
