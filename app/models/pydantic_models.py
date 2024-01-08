from pydantic import BaseModel
from datetime import datetime


# エンドポイント'create_user_id'のモデル
class UserIdResponse(BaseModel):
    userId: str


# エンドポイント'read_document_file'メソッドのモデル
class DocumentFileResponse(BaseModel):
    text: str


# エンドポイント'calculate_similarity'メソッドのモデル
class SimilarityRequest(BaseModel):
    user_id: str
    keywords: list[str]
    text: str


class SimilarityResponse(BaseModel):
    sentences: list[str]
    similar_infomations: list[dict[str, str | list[float]]]


# エンドポイント'determine_similar_keyword'メソッドのモデル
class SimilarKeywordRequest(BaseModel):
    user_id: str
    sentences: list[str]
    similar_infomations: list[dict[str, str | list[float]]]


class SimilarKeywordResponse(BaseModel):
    results: list[dict[str, str | float]]


# エンドポイント'update_last_accessed_at'のモデル
class LastAccessedAtResponse(BaseModel):
    message: str


# エンドポイント'read_all_users'のモデル
class AllUsersRequest(BaseModel):
    password: str


class AllUsersResponse(BaseModel):
    results: list[dict[str, int | str | datetime]]


# エンドポイント'read_user_count'のモデル
class UserCountResponse(BaseModel):
    user_count: int


# エンドポイント'create_user_table'のモデル
class UserTableResponse(BaseModel):
    message: str
