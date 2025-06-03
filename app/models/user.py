from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Optional, Annotated, List
from . import GroupUserLink
from uuid import UUID, uuid4

class UserBase(SQLModel):
    username: Annotated[str, StringConstraints(min_length=4, max_length=64)] = Field(unique=True, index=True)
    email: Optional[EmailStr] = None
    full_name: Optional[Annotated[str, StringConstraints(min_length=6, max_length=64)]] = None

class UserLogin(SQLModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8, max_length=64)]

class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    isActive: bool = False
    hashed_password: str = Field()
    items: List["Item"] = Relationship(back_populates='user')
    groups: List["Group"] = Relationship(back_populates='users', link_model=GroupUserLink)

class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(min_length=8, max_length=64)]

class UserRead(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

from .item import Item
from .group import Group
