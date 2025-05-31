from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr, StringConstraints
from typing import Optional, Annotated

class UserBase(SQLModel):
    username: Annotated[str, StringConstraints(min_length=4, max_length=64)] = Field(unique=True, index=True)
    email: Optional[EmailStr] = None
    full_name: Optional[Annotated[str, StringConstraints(min_length=6, max_length=64)]] = None

class UserLogin(SQLModel):
    email: EmailStr
    password: Annotated[str, StringConstraints(min_length=8, max_length=64)]


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    isActive: bool = False
    hashed_password: str = Field()

class UserCreate(UserBase):
    password: Annotated[str, StringConstraints(min_length=8, max_length=64)]

class UserRead(UserBase):
    id: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
