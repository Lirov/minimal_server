from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.todo import TodoCreate, TodoOut
from app.controllers.todos_controller import list_todos, create_todo, delete_todo
from app.dependencies.auth import get_current_subject

router = APIRouter()

@router.get("/", response_model=List[TodoOut])
def get_todos(sub: str = Depends(get_current_subject)):
    return list_todos(sub)

@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def post_todo(payload: TodoCreate, sub: str = Depends(get_current_subject)):
    return create_todo(sub, payload)

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_todo(todo_id: str, sub: str = Depends(get_current_subject)):
    ok = delete_todo(sub, todo_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return
