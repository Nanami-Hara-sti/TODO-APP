import datetime as DateTime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import Depends
# import schemas
# import crud
from app.database import SessionLocal, engine, get_db


class todos(BaseModel):
    id: int = Field(..., example="TodoのID")
    title: str = Field(..., max_length=255, example="タイトル")
    description: str = Field(None, max_length=1000, example="詳細")
    status: str = Field("未着手", max_length=20, example="ステータス")
    created_at: DateTime.datetime = Field(..., example="作成日時")
    updated_at: DateTime.datetime = Field(..., example="更新日時")

app = FastAPI()

# CORSを許可するオリジン（Reactアプリが動作するURL)
origins = ["http://localhost:3000"]

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 許可するオリジン
    allow_credentials=True,      # クッキーを許可するか
    allow_methods=["*"],         # 全てのHTTPメソッドを許可
    allow_headers=["*"],         # 全てのHTTPヘッダーを許可
)

fake_db = []
id_counter = 0

@app.post("/items/") # ← response_modelを削除
def create_item(db: Session = Depends(get_db)):
    # 関数の内容も、エラーにならないように一時的に単純化する
    return {"message": "This endpoint is temporarily disabled."}
# @app.post("/todos", response_model=schemas.Todo)
# def create_todo(todo: schemas.TodoCreate):
#     """
#     新しいTodoアイテムを作成します。

#     - Request Body: `schemas.TodoCreate` に基づいてバリデーションされます。
#     - Response Body: `schemas.Todo` に基づいてフォーマットされます。
#     """
#     global id_counter
    
#     # IDと日時をサーバー側で生成
#     id_counter += 1
#     current_time = datetime.datetime.now()

#     # レスポンス用のデータモデルを作成
#     new_todo = schemas.Todo(
#         id=id_counter,
#         title=todo.title,
#         description=todo.description,
#         status=todo.status,
#         created_at=current_time,
#         updated_at=current_time,
#     )

#     # 簡易DBに追加
#     fake_db.append(new_todo)
    
#     # 作成したTodoを返す
#     return new_todo

# @app.get("/todos", response_model=list[schemas.Todo])
# def read_todos():
#     """
#     すべてのTodoアイテムを取得します。
#     """
#     return fake_db

@app.get("/")
async def index():
    return {"message": "Welcome to the Todo API"}

@app.post("/todos")
async def create_todo(todos: todos):
    return {"todos": [todos]}