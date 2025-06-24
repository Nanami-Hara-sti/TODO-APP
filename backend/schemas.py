import datetime
from pydantic import BaseModel, Field
from typing import Optional

class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None  
    status: str = "未着手"

class TodoCreate(TodoBase):
    pass  

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class Todo(TodoBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True