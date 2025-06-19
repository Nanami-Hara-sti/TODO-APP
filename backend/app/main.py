import datetime as DateTime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

class todos(BaseModel):
    id: int = Field(..., example="TodoのID")
    title: str = Field(..., max_length=255, example="タイトル")
    description: str = Field(None, max_length=1000, example="詳細")
    status: str = Field("未着手", max_length=20, example="ステータス")
    created_at: DateTime.datetime = Field(..., example="作成日時")
    updated_at: DateTime.datetime = Field(..., example="更新日時")

app = FastAPI()

@app.get("/")
async def index():
    return {"message": "Welcome to the Todo API"}

@app.post("/todos")
async def create_todo(todos: todos):
    return {"todos": [todos]}