"""intento#4

Revision ID: dcca8e27d7db
Revises: c2dad3d2a9ec
Create Date: 2025-11-10 12:57:02.673233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dcca8e27d7db'
down_revision: Union[str, Sequence[str], None] = 'c2dad3d2a9ec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tabla",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.Unicode(200)),
        schema="public"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tabla")