from typing import Union
from .validation import Item, ItemBase

class ItemController:
    @classmethod
    def get_item(self, item_id: int, q: Union[str, None] = None):
        return {"item_id": item_id, "q": q}
    
    @classmethod
    def create_item(self, item: ItemBase):
        return {"item_name": item.name}
    
    @classmethod
    def get_all_items(self, q: Union[str, None] = None):
        return {"item_name": q}

    @classmethod
    def update_item(self, item_id: int, item: ItemBase):
        return {"item_name": item.name, "item_id": item_id}

    @classmethod
    def delete_item(self, item_id: int):
        return {"item_id": item_id}