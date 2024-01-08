import fitz
import chardet
from io import BytesIO
from docx import Document
from odf import text, teletype
from odf.opendocument import OpenDocument, load
from odf.element import Element
from ebooklib import epub, ITEM_DOCUMENT
from ebooklib.epub import EpubBook
from bs4 import BeautifulSoup
from tempfile import NamedTemporaryFile


# ドキュメントファイルを操作するためのクラス
class DocumentFile:
    def __init__(self, file: BytesIO, filename: str) -> None:
        self.file = file
        self.filename = filename

    # 改行コードを挟んでパラグラフを結合する
    def __join_paragraphs(self, paragraphs: list[str]) -> str:
        return "\n".join(paragraphs)

    # 文字コードを自動判定した上で、ファイルからコンテンツを取得する
    def __get_contents(self) -> str:
        # ファイルを読み込む
        contents: bytes = self.file.read()
        # 文字コードを判定する
        encoding: str = chardet.detect(contents)["encoding"]

        # 復号化したコンテンツを返す
        return contents.decode(encoding)

    # DOCXファイルを読み込み、テキストを返す
    def __read_docx(self) -> str:
        # DOCXファイルを読み込む
        document = Document(self.file)
        # ファイルからパラグラフを取得する
        paragraphs: list[str] = list(map(lambda p: p.text, document.paragraphs))

        # パラグラフを結合して返す
        return self.__join_paragraphs(paragraphs)

    # ODTファイルを読み込み、テキストを返す
    def __read_odt(self) -> str:
        # ODTファイルを読み込む
        document: OpenDocument = load(self.file)
        # ファイルからパラグラフをオブジェクトとして取得する
        elements: list[Element] = document.getElementsByType(text.P)
        # オブジェクトからテキストを取得する
        paragraphs: list[str] = list(map(lambda p: teletype.extractText(p), elements))

        # パラグラフを結合して返す
        return self.__join_paragraphs(paragraphs)

    # PDFファイルを読み込み、テキストを返す
    def __read_pdf(self) -> str:
        # PDFファイルを読み込む
        pdf_file = BytesIO(self.file.read())
        # ファイルを開く
        document = fitz.open(stream=pdf_file, filetype="pdf")

        # ページごとにテキストを取得する（改行コードは含まれている）
        return "".join(list(map(lambda p: p.get_text(), document)))

    # TXTファイルを読み込み、テキストを返す
    def __read_txt(self) -> str:
        # 改行コードは含まれている
        return self.__get_contents()

    # EPUBファイルを読み込み、テキストを返す
    def __read_epub(self) -> str:
        # EPUBファイルを読み込む
        contents: bytes = self.file.read()
        items: list[any]
        paragraphs: list[str] = []

        # ランダムな名前の一時ファイルを作成する（例: tmpetu4sgnn.epub）
        with NamedTemporaryFile(delete=True, suffix=".epub") as tempfile:
            book: EpubBook

            # EPUBファイルの内容を一時ファイルに書き込む
            tempfile.write(contents)
            # 一時ファイルを保存する
            tempfile.flush()
            # 保存した一時ファイルを読み込む
            book = epub.read_epub(tempfile.name, {"ignore_ncx": True})
            # オブジェクトから要素を取得する
            items = list(book.get_items_of_type(ITEM_DOCUMENT))

        for item in items:
            # 要素を解析する（あえてlxmlを指定しているため、コンソールに警告が出る）
            soup = BeautifulSoup(item.content, "lxml")
            # テキストを取得する
            paragraphs.append(soup.get_text())

        # パラグラフを結合して返す
        return self.__join_paragraphs(paragraphs)

    # HTMLファイルを読み込み、テキストを返す
    def __read_html(self) -> str:
        # HTMLファイルから要素を取得する
        decoded_contents: str = self.__get_contents()
        # 要素を解析する
        soup = BeautifulSoup(decoded_contents, "html.parser")

        # JavaScriptとCSSを除去する
        for script in soup(["script", "style"]):
            script.extract()

        # テキストを返す
        return soup.get_text()

    # ドキュメントファイルを読み込む
    def read_document_file(self) -> str:
        # ファイル名から拡張子を取得する
        extension: str = self.filename.split(".")[-1]
        # 拡張子と使用するメソッドを紐付ける
        extension_method: dict[str, any] = {
            "docx": self.__read_docx,
            "odt": self.__read_odt,
            "pdf": self.__read_pdf,
            "txt": self.__read_txt,
            "epub": self.__read_epub,
            "html": self.__read_html,
        }

        try:
            # 拡張子に対応するメソッドを実行する
            return extension_method[extension]()
        except KeyError:
            raise KeyError("対応していない拡張子です。")
