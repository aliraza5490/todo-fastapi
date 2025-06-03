from uuid import UUID, uuid4
from pydantic import EmailStr
from sqlmodel import SQLModel
from typing import Optional, List
from sqlmodel import Relationship, Field
from . import GroupUserLink

class GroupBase(SQLModel):
    name: str
    description: Optional[str] = None


class GroupInvite(SQLModel):
    email: EmailStr
    message: Optional[str] = None


class Group(GroupBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    admin: UUID = Field(foreign_key="user.id")
    users: List["User"] = Relationship(back_populates='groups', link_model=GroupUserLink)


from .user import User
