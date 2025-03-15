"""create items table

Revision ID: 464efd96205a
Revises:
Create Date: 2025-03-15 15:36:13.419567

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "464efd96205a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "items",
        sa.Column("id", sa.UUID, primary_key=True),
        sa.Column(
            "title",
            sa.String(255),
            index=True,
        ),
        sa.Column("description", sa.String),
        sa.Column("resolved", sa.Boolean, default=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table(table_name="items")
