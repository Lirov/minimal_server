import uuid
from typing import List

class TodoService:
    """Minimal in-memory todo store keyed by user_id (from JWT 'sub')."""
    def __init__(self) -> None:
        self._store: dict[str, list[dict]] = {}

    # list_for_user()
    def list_for_user(self, user_id: str) -> list[dict]:
        return self._store.get(user_id, [])

    # create_for_user()
    def create_for_user(self, user_id: str, title: str, completed: bool = False) -> dict:
        todo = {"id": str(uuid.uuid4()), "title": title, "completed": completed}
        self._store.setdefault(user_id, []).append(todo)
        return todo

    # delete_for_user()
    def delete_for_user(self, user_id: str, todo_id: str) -> bool:
        items = self._store.get(user_id, [])
        before = len(items)
        items[:] = [t for t in items if t["id"] != todo_id]
        self._store[user_id] = items
        return len(items) < before

todo_service = TodoService()
