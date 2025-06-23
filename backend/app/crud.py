import datetime as DateTime
from typing import List, Optional
from .schemas import TodoCreate, Todo, TodoUpdate

# メモリ上のDB（本来はDB操作を記述）
fake_db: List[Todo] = []
id_counter = 0

def create_todo(todo: TodoCreate) -> Todo:
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

def read_todos() -> List[Todo]:
    return fake_db

def read_todo(todo_id: int) -> Optional[Todo]:
    for todo in fake_db:
        if todo.id == todo_id:
            return todo
    return None

def update_todo(todo_id: int, todo: TodoCreate) -> Optional[Todo]:
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
    return None

def delete_todo(todo_id: int) -> bool:
    for idx, t in enumerate(fake_db):
        if t.id == todo_id:
            del fake_db[idx]
            return True
    return False