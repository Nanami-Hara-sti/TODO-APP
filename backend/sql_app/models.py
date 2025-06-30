# SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sql_app.database import Base
import datetime

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default="未着手")
    # UTC時刻で保存するように明示的に設定
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Todo(id={self.id}, title='{self.title}', status='{self.status}')>"

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ship_name = Column(String(255), nullable=False)
    freight = Column(String(255))

    def __repr__(self):
        return f"<Order(id={self.id}, ship_name='{self.ship_name}', freight='{self.freight}')>"