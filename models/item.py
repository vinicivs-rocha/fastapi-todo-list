import uuid
from datetime import datetime

from sqlmodel import SQLModel, Field


class ItemBase(SQLModel):
    title: str = Field(max_length=255, index=True)
    description: str | None = None
    resolved: bool = False


class Item(ItemBase, table=True):
    __tablename__ = "items"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    deleted_at: datetime | None = None
