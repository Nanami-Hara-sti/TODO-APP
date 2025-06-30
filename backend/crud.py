from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from sql_app import models
from schemas import TodoCreate, Todo
import datetime

def create_todo(db: Session, todo: TodoCreate) -> models.Todo:
    db_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        status=todo.status
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def read_todos(db: Session):
    return db.query(models.Todo).all()

def read_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()

def update_todo(db: Session, todo_id: int, todo: TodoCreate):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        return None
    db_todo.title = todo.title
    db_todo.description = todo.description
    db_todo.status = todo.status
    # 更新時刻を明示的にUTCで設定
    db_todo.updated_at = datetime.datetime.utcnow()
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo is None:
        return False
    db.delete(db_todo)
    db.commit()
    return True