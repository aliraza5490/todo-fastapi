from typing import Annotated, Optional
from pydantic import StringConstraints
from sqlmodel import SQLModel, Field

class ItemBase(SQLModel):
    name: Annotated[str, StringConstraints(min_length=2, max_length=100)]
    description: Annotated[str, StringConstraints(max_length=500)] = None
    is_done: bool

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

