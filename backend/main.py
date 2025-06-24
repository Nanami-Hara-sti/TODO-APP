import datetime as DateTime
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import crud
import schemas
from sqlalchemy.orm import Session
from sql_app.database import engine, get_db
from sql_app import models as sql_models

sql_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class todos(BaseModel):
    id: int = Field(..., example="TodoのID")
    title: str = Field(..., max_length=255, example="タイトル")
    description: str = Field(None, max_length=1000, example="詳細")
    status: str = Field("未着手", max_length=20, example="ステータス")
    created_at: DateTime.datetime = Field(..., example="作成日時")
    updated_at: DateTime.datetime = Field(..., example="更新日時")

# CORSを許可するオリジン（Reactアプリが動作するURL)
origins = [
    "http://localhost:3000",
    "http://localhost:3001"
]

# CORSミドルウェアを追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,      
    allow_methods=["*"],         
    allow_headers=["*"],         
)

class TodoBase(BaseModel):
    title: str = Field(..., max_length=255, example="タイトル")
    description: str = Field(None, max_length=1000, example="詳細")
    status: str = Field("未着手", max_length=20, example="ステータス")

class TodoCreate(TodoBase):
    pass

class Todo(TodoBase):
    id: int
    created_at: DateTime.datetime
    updated_at: DateTime.datetime

@app.get("/")
async def index():
    return {"message": "Welcome to the Todo API"}

fake_db = []
id_counter = 0

# Create
@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    global id_counter
    id_counter += 1
    now = DateTime.datetime.now()
    new_todo = Todo(
        id=id_counter,
        title=todo.title,
        description=todo.description,
        status=todo.status,
        created_at=now,
        updated_at=now,
    )
    fake_db.append(new_todo)
    return new_todo

# Read All
@app.get("/todos", response_model=list[Todo])
def read_todos():
    return fake_db

# Read One
@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    for todo in fake_db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

# Update
@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate):
    for idx, t in enumerate(fake_db):
        if t.id == todo_id:
            updated_todo = Todo(
                id=todo_id,
                title=todo.title,
                description=todo.description,
                status=todo.status,
                created_at=t.created_at,
                updated_at=DateTime.datetime.now(),
            )
            fake_db[idx] = updated_todo
            return updated_todo
    raise HTTPException(status_code=404, detail="Todo not found")

# Delete
@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int):
    for idx, t in enumerate(fake_db):
        if t.id == todo_id:
            del fake_db[idx]
            return {"result": "success"}
    raise HTTPException(status_code=404, detail="Todo not found")