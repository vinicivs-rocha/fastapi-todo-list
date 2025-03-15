from datetime import datetime
from uuid import UUID

from models.item import ItemBase


class ItemPublic(ItemBase):
    id: UUID
    created_at: datetime
