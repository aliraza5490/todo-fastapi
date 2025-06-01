from fastapi import HTTPException
from typing import Union
from ...models.item import Item, ItemBase
from sqlmodel import Session, select
from ...models.user import User

class ItemController:
    @classmethod
    def get_item(self, item_id: int, user: User, session: Session):
        itemData = session.exec(select(Item).where(Item.id == item_id)).first()
        if not itemData:
            raise HTTPException(
                status_code=404,
                detail=f"Item with id {item_id} not found."
            )
        return itemData
    
    @classmethod
    def create_item(self, item: ItemBase, user: User, session: Session):
        item_data = Item(
            **item.model_dump(),
            user_id=user.id
        )
        session.add(item_data)
        session.commit()
        return {"item_name": item.name}
    
    @classmethod
    def get_all_items(self, user: User, session: Session, q: Union[str, None] = None):
        query = select(Item).where(Item.user_id == user.id)
        if q:
            query = query.where(Item.name.ilike(f"%{q}%"))
        items = session.exec(query).all()
        return {"items": items}

    @classmethod
    def update_item(self, item_id: int, item: ItemBase, user: User, session: Session):
        itemData = session.exec(select(Item).where(Item.id == item_id, Item.user_id == user.id)).first()
        if not itemData:
            raise HTTPException(
                status_code=404,
                detail=f"Item with id {item_id} not found."
            )
        
        # Only update fields that are provided in the request
        update_data = item.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(itemData, key, value)
        
        session.add(itemData)
        session.commit()
        session.refresh(itemData)
        
        return {"item_name": itemData.name, "item_id": item_id}

    @classmethod
    def delete_item(self, item_id: int, user: User, session: Session):
        itemData = session.exec(select(Item).where(Item.id == item_id, Item.user_id == user.id)).first()
        if not itemData:
            raise HTTPException(
                status_code=404,
                detail=f"Item with id {item_id} not found."
            )
        session.delete(itemData)
        session.commit()
        return {"item_id": item_id}