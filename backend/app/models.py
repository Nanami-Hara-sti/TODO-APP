# SQLAlchemy モデル

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Todo(Base):
    __tablename__ = "todos" 

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="未着手")
    created_at = Column(DateTime(timezone=True), server_default=func.now()) 
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', status='{self.status}')>"