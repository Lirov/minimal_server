from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    __tablename__ = "user"
    
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
