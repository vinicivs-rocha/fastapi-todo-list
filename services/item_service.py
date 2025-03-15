from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import HTTPException, Depends
from sqlmodel import select, or_, col

from db.pg import SessionDep
from dto.item_create import ItemCreate
from dto.item_update import ItemUpdate
from models.item import Item


class ItemService:
    session: SessionDep

    def __init__(self, session: SessionDep):
        self.session = session

    def create_item(self, item: ItemCreate) -> Item:
        db_item = Item.model_validate(item)
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        return db_item

    def list_items(self, page=0, length=10, query: str | None = None) -> list[Item]:
        statement = (
            select(Item)
            .limit(length)
            .offset(page * length)
            .where(Item.deleted_at == None)
        )

        if query is not None:
            statement = statement.where(
                or_(
                    col(Item.title).contains(f"%{query}%"),
                    col(Item.description).contains(f"%{query}%"),
                )
            )

        return self.session.exec(statement).all()

    def update_item(self, item_id: UUID, item: ItemUpdate) -> None:
        db_item = self.session.exec(
            select(Item).where(Item.id == item_id).where(Item.deleted_at == None),
        ).one()
        if not db_item:
            raise HTTPException(status_code=404, detail=db_item.model_dump())
        db_item.sqlmodel_update(item.model_dump())
        self.session.add(db_item)
        self.session.commit()

    def delete_item(self, item_id: UUID) -> None:
        db_item = self.session.exec(
            select(Item).where(Item.id == item_id).where(Item.deleted_at == None),
        ).one()
        if not db_item:
            raise HTTPException(status_code=404, detail="Item not found")
        db_item.sqlmodel_update({"deleted_at": datetime.now()})
        self.session.add(db_item)
        self.session.commit()


ItemServiceDep = Annotated[ItemService, Depends(ItemService)]
