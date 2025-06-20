import datetime as DateTime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

class todos(BaseModel):
    id: int = Field(..., example="TodoのID")
    title: str = Field(..., max_length=255, example="タイトル")
    description: str = Field(None, max_length=1000, example="詳細")
    status: str = Field("未着手", max_length=20, example="ステータス")
    created_at: DateTime.datetime = Field(..., example="作成日時")
    updated_at: DateTime.datetime = Field(..., example="更新日時")

app = FastAPI()

# CORSを許可するオリジン（Reactアプリが動作するURL）のリスト
origins = [
    "http://localhost:3000", # Reactのデフォルト開発サーバー
    "http://localhost:3001", # create-react-appが使う可能性のある他のポート
    "http://127.0.0.1:3000",
]

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 許可するオリジン
    allow_credentials=True,      # クッキーを許可するか
    allow_methods=["*"],         # 全てのHTTPメソッドを許可
    allow_headers=["*"],         # 全てのHTTPヘッダーを許可
)

@app.get("/")
async def index():
    return {"message": "Welcome to the Todo API"}

@app.post("/todos")
async def create_todo(todos: todos):
    return {"todos": [todos]}