from typing import Annotated, Optional, ForwardRef
from pydantic import StringConstraints
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID, uuid4

class ItemBase(SQLModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=100)]
    description: Annotated[str, StringConstraints(max_length=500)] = None
    is_done: bool

class Item(ItemBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID | None = Field(default=None, foreign_key="user.id")
    user: "User" = Relationship(back_populates="items")

from .user import User
