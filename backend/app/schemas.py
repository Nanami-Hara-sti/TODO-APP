import datetime
from pydantic import BaseModel, Field
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: str | None = None  
    status: str = "未着手"

class TodoCreate(TodoBase):
    pass  

class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None

class Todo(TodoBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True