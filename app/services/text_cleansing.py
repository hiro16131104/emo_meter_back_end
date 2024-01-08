from functools import partial
from typing import Generator
from ja_sentence_segmenter.common.pipeline import make_pipeline
from ja_sentence_segmenter.concatenate.simple_concatenator import concatenate_matching
from ja_sentence_segmenter.normalize.neologd_normalizer import normalize
from ja_sentence_segmenter.split.simple_splitter import split_newline, split_punctuation

# オリジナルのクラスをインポート
from .utility import Utility


# テキストクレンジング（前処理）を行うためのクラス
class TextCleansing:
    def __init__(self, text: str) -> None:
        # 加工前のテキスト
        self.text = text

    # 各文から改行コード（CRとLF）を除去する
    def __remove_newline_codes(self, sentences: list[str]) -> list[str]:
        return list(map(lambda x: Utility.remove_chars(x, [r"\r", r"\n"]), sentences))

    # 日本語のテキストを文に分割する
    def segment_into_sentences(self) -> list[str]:
        # 句点（。!?）を基に文章を分割する関数を定義
        split_by_punctuation: partial[Generator[str, None, None]] = partial(
            split_punctuation, punctuations=r"。！？.!?"
        )
        # 末尾が「の」で終わる文を次の文と結合する関数を定義
        concatenate_if_tail_is_no: partial[Generator[str, None, None]] = partial(
            concatenate_matching,
            former_matching_rule=r"^(?P<result>.+)(の)$",
            remove_former_matched=False,
        )
        # 処理パイプラインを作成
        # normalize: テキストの正規化, split_newline: 改行で分割
        create_segmentation_pipeline: Generator[str, None, None] = make_pipeline(
            normalize, split_newline, concatenate_if_tail_is_no, split_by_punctuation
        )
        sentences: list[str] = list(create_segmentation_pipeline(self.text))

        return self.__remove_newline_codes(sentences)
