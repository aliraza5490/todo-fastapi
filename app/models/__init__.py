from uuid import UUID
from sqlmodel import SQLModel, Field


class GroupUserLink(SQLModel, table=True):
    group_id: UUID | None = Field(default=None, foreign_key="group.id", primary_key=True)
    user_id: UUID | None = Field(default=None, foreign_key="user.id", primary_key=True)
