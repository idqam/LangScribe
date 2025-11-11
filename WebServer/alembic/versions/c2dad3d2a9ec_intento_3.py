"""intento#3

Revision ID: c2dad3d2a9ec
Revises: 59a3b6f89eb8
Create Date: 2025-11-10 12:49:23.232299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2dad3d2a9ec'
down_revision: Union[str, Sequence[str], None] = '59a3b6f89eb8'
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
