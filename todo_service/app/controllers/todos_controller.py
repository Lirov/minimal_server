from app.schemas.todo import TodoCreate, TodoOut
from app.services.todo_service import todo_service

# list_todos()
def list_todos(user_id: str):
    return todo_service.list_for_user(user_id)

# create_todo()
def create_todo(user_id: str, payload: TodoCreate):
    return todo_service.create_for_user(user_id, payload.title, payload.completed)

# delete_todo()
def delete_todo(user_id: str, todo_id: str) -> bool:
    return todo_service.delete_for_user(user_id, todo_id)
