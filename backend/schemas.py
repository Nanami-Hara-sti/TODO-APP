import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from enum import Enum

class TodoStatus(str, Enum):
    """TODOステータスの列挙型"""
    NOT_STARTED = "未着手"
    IN_PROGRESS = "進行中"
    COMPLETED = "完了"

class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="TODOのタイトル")
    description: Optional[str] = Field(None, max_length=1000, description="TODOの詳細説明")
    status: TodoStatus = Field(TodoStatus.NOT_STARTED, description="TODOのステータス")

class TodoCreate(TodoBase):
    pass  

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TodoStatus] = None

class Todo(TodoBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
        # JSON serialization時にISO 8601形式（UTC）で出力
        json_encoders = {
            datetime.datetime: lambda dt: dt.isoformat() + 'Z' if dt else None
        }