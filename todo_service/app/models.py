from sqlmodel import SQLModel, Field
from typing import Optional

class Todo(SQLModel, table=True):
    __tablename__ = "todo"
    
    id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    title: str
    completed: bool = Field(default=False)
