from uuid import UUID
from fastapi import APIRouter, Depends
from typing import Union
from ...models.item import ItemBase
from ...utilities.tags import Tags
from .service import ItemService
from ...utilities.auth import get_user_from_token
from ...models.user import User
from sqlmodel import Session
from ...utilities.db import get_session

items_router = APIRouter(prefix="/items", tags=[Tags.items], dependencies=[Depends(get_user_from_token)])

@items_router.post("/")
def create_item(item: ItemBase, user: User = Depends(get_user_from_token), session: Session = Depends(get_session)):
    return ItemService.create_item(item, user, session)

@items_router.get("/{item_id}")
def read_item(item_id: UUID, user: User = Depends(get_user_from_token), session: Session = Depends(get_session)):
    return ItemService.get_item(item_id, user, session)

@items_router.get("/")
def read_all_item(q: Union[str, None] = None, user: User = Depends(get_user_from_token), session: Session = Depends(get_session)):
    return ItemService.get_all_items(user, session, q)

@items_router.put("/{item_id}")
def update_item(item_id: UUID, item: ItemBase, user: User = Depends(get_user_from_token), session: Session = Depends(get_session)):
    return ItemService.update_item(item_id, item, user, session)

@items_router.delete("/{item_id}")
def delete_item(item_id: UUID, user: User = Depends(get_user_from_token), session: Session = Depends(get_session)):
    return ItemService.delete_item(item_id, user, session)
