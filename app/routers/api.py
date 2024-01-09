from fastapi import APIRouter, Form, UploadFile, HTTPException
from datetime import datetime

# オリジナルのクラスをインポート
from config.config import Config
from ..models.pydantic_models import *
from ..models.dynamodb_models import UserModel
from ..services.document_file import DocumentFile
from ..services.utility import Utility
from ..services.text_cleansing import TextCleansing
from ..services.semantic_search import SemanticSearch
from ..services.similar_keyword import SimilarKeyword
from ..crud.table_operation import TableOperation
from ..crud.user_operation import UserOperation


# 共通変数の定義
router = APIRouter()


# ユーザーIDを生成するエンドポイント
@router.get("/api/create_user_id", response_model=UserIdResponse)
def create_user_id() -> UserIdResponse:
    user_id = ""

    while True:
        # ユーザーIDを生成する（20文字のランダムな文字列）
        user_id = Utility.generate_random_string(20)
        # ユーザーIDが重複していなければループを抜ける
        if not UserOperation.read_user(user_id):
            break

    # レコードを作成する
    UserOperation.create_user(user_id)
    return {"userId": user_id}


# ドキュメントファイルを読み込むエンドポイント
@router.post("/api/read_document_file", response_model=DocumentFileResponse)
def read_document_file(
    user_id: str = Form(...), file: UploadFile = Form(...)
) -> DocumentFileResponse:
    text = ""

    # ドキュメントファイルを読み込む
    try:
        document_file = DocumentFile(file.file, file.filename)
        text = document_file.read_document_file()
    except KeyError as ex:
        raise HTTPException(400, str(ex))

    # ドキュメントファイルの内容を返す
    return {"text": text}


# 文章とキーワードの類似度を計算するエンドポイント
@router.post("/api/calculate_similarity", response_model=SimilarityResponse)
def calculate_similarity(request: SimilarityRequest) -> SimilarityResponse:
    text: str = request.text
    keywords: list[str] = request.keywords

    # テキストの文字数が上限を超えている場合はエラーを返す
    if len(text) > Config.max_word_count:
        raise HTTPException(400, "文字数が上限を超えています。")

    # テキストを文に分割する
    sentences: list[str] = TextCleansing(text).segment_into_sentences()
    similar_infomations: list[dict[str, str | list[float]]] = []

    # クラス変数に文章と学習済みモデルを格納する
    SemanticSearch.set_sentences(sentences)

    print("+++test+++")
    import glob
    files = glob.glob("./*")
    for file in files:
        print(file)

    SemanticSearch.set_learned_model(Config.model_name)

    for keyword in keywords:
        similar_infomation: dict[str, str | list[float]] = {}
        semantic_search = SemanticSearch(keyword)

        # 文章とキーワードの類似度を計算する
        semantic_search.calculate_similarity()
        # キーワードと類似度（計算結果）を格納する
        similar_infomation = {
            "keyword": keyword,
            "similarities": semantic_search.similarities,
        }
        similar_infomations.append(similar_infomation)

    # 文章、キーワード、類似度を返す
    return {"sentences": sentences, "similar_infomations": similar_infomations}


# 各文章に対して類似度が最も高いキーワードを決定するエンドポイント
@router.post("/api/determine_similar_keyword", response_model=SimilarKeywordResponse)
def determine_similar_keyword(
    request: SimilarKeywordRequest,
) -> SimilarKeywordResponse:
    sentences: list[str] = request.sentences
    similar_infomations: list[
        dict[str, str | list[float]]
    ] = request.similar_infomations
    similar_keyword = SimilarKeyword(sentences, similar_infomations)
    # 各文章に対して類似度が最も高いキーワードを決定する
    results: list[dict[str, str | float]] = similar_keyword.determine_similar_keyword(
        Config.minimum_similarity
    )

    # 文、キーワード、類似度を格納したリストを返す
    return {"results": results}


# 最終アクセス日時を更新するエンドポイント
@router.put(
    "/api/update_last_accessed_at/{user_id}", response_model=LastAccessedAtResponse
)
def update_last_accessed_at(user_id: str) -> LastAccessedAtResponse:
    # ユーザーIDが存在する場合
    if UserOperation.read_user(user_id):
        # レコードを更新する
        UserOperation.update_user(user_id)
        return {"message": "最終アクセス日時を更新しました。"}
    else:
        # ユーザーIDが存在しない場合はエラーを返す
        raise HTTPException(400, "ユーザーIDが存在しません。")


# ユーザーテーブルの全てのレコードを取得するエンドポイント
@router.post("/api/read_all_users", response_model=AllUsersResponse)
def read_all_users(request: AllUsersRequest) -> AllUsersResponse:
    password: str = request.password
    users: list[UserModel] = []
    results: list[dict[str, int | str | datetime]] = []

    # パスワードが違う場合はエラーを返す
    if password != Config.password_admin:
        raise HTTPException(400, "パスワードが違います。")

    # ユーザーテーブルから全てのレコードを取得する
    users = UserOperation.read_all_users()

    # 取得したレコードを辞書に変換する
    for index, user in enumerate(users):
        result = {
            "no": index + 1,
            "user_id": user.user_id,
            "created_at": user.created_at,
            "last_accessed_at": user.last_accessed_at,
        }
        results.append(result)

    return {"results": results}


# ユーザーテーブルのレコード件数を取得するエンドポイント
@router.get("/api/read_user_count", response_model=UserCountResponse)
def read_user_count() -> UserCountResponse:
    # ユーザーテーブルのレコード件数を取得する
    user_count: int = UserOperation.read_user_count()
    return {"user_count": user_count}


# DBにテーブルを作成するエンドポイント
@router.get("/api/create_user_table", response_model=UserTableResponse)
def create_user_table() -> UserTableResponse:
    # テーブルが存在する場合は処理を抜ける
    if TableOperation.exist_user_table():
        return {"message": "テーブルは既に存在します。"}

    # テーブルを作成する
    TableOperation.create_user_table()
    return {"message": "テーブルを作成しました。"}
