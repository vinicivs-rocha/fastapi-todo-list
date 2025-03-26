from uuid import UUID

from fastapi import APIRouter

from dto.item_create import ItemCreate
from dto.item_public import ItemPublic
from dto.item_update import ItemUpdate
from services.item_service import ItemServiceDep

router = APIRouter(prefix="/items")


@router.post("/", status_code=201)
def create_item(item: ItemCreate, item_service: ItemServiceDep):
    created = item_service.create_item(item=item)
    return {
        "id": created.id,
        "message": "Item created successfully",
    }


@router.get("/", response_model=list[ItemPublic])
def list_items(
    item_service: ItemServiceDep, query: str | None = None, resolved: bool = False
):
    return item_service.list_items(query=query, resolved=resolved)


@router.put("/{item_id}")
def update_item(item_id: UUID, item: ItemUpdate, item_service: ItemServiceDep):
    item_service.update_item(item_id=item_id, item=item)
    return {
        "message": "Item updated successfully",
    }


@router.delete("/{item_id}")
def delete_item(item_id: UUID, item_service: ItemServiceDep):
    item_service.delete_item(item_id=item_id)
    return {
        "message": "Item deleted successfully",
    }
