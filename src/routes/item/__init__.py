from fastapi import APIRouter, Depends
from typing import Union
from .validation import Item
from ...utilities.tags import Tags
from .controllers import ItemController
from ...utilities.auth import get_user_from_token

items_router = APIRouter(prefix="/items", tags=[Tags.items], dependencies=[Depends(get_user_from_token)])

@items_router.post("/")
def create_item(item: Item):
    return ItemController.create_item(item)

@items_router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return ItemController.get_item(item_id, q)

@items_router.get("/")
def read_all_item(q: Union[str, None] = None):
    return ItemController.get_all_items(q)

@items_router.patch("/{item_id}")
def update_item(item_id: int, item: Item):
    return ItemController.update_item(item_id, item)

@items_router.delete("/{item_id}")
def delete_item(item_id: int):
    return ItemController.delete_item(item_id)
