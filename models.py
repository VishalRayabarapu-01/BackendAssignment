from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from pydantic import EmailStr, validator

class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    role: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    projects: List["Project"] = Relationship(back_populates="owner", sa_relationship_kwargs={"cascade": "all, delete"})

class UserCreate(UserBase):
    password: str

    @validator("password")
    def validate_password(cls, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number")
        if not any(char in "!@#$%^&*()_+" for char in password):
            raise ValueError("Password must contain at least one special character")
        return password

class UserRead(UserBase):
    id: int

class Token(SQLModel):
    access_token: str
    token_type: str

class TokenData(SQLModel):
    username: Optional[str] = None
    role: Optional[str] = None

class ProjectBase(SQLModel):
    name: str
    description: Optional[str] = None

class Project(ProjectBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="projects")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

class ProjectUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
