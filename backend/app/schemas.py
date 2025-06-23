import datetime
from pydantic import BaseModel

# --- ベースとなるスキーマ ---
# 他のスキーマで共通して利用するフィールドを定義します。
# これを継承することで、同じ記述を繰り返す必要がなくなります。
class TodoBase(BaseModel):
    title: str
    description: str | None = None  # descriptionは任意(NoneでもOK)
    status: str


# --- データ作成時に利用するスキーマ ---
# フロントエンドからPOSTリクエストで受け取るデータの構造を定義します。
# idや日時はバックエンドで生成するため、ここには含めません。
class TodoCreate(TodoBase):
    pass  # TodoBaseのフィールドをそのまま利用


# --- データを読み取る（APIレスポンスで返す）際に利用するスキーマ ---
# APIがフロントエンドに返すデータの構造を定義します。
# DBで自動採番されたidや、登録日時なども含みます。
class Todo(TodoBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    # PydanticモデルがORMモデル(SQLAlchemy等)と連携するための設定
    # これにより、DBから取得したオブジェクトを自動でこのスキーマに変換できます。
    class Config:
        from_attributes = True