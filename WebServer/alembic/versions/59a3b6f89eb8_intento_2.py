"""intento#2

Revision ID: 59a3b6f89eb8
Revises: 38a8d5ee7297
Create Date: 2025-11-10 12:28:00.275041

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "59a3b6f89eb8"
down_revision: str | Sequence[str] | None = "38a8d5ee7297"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "tabla",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.Unicode(200)),
        schema="public",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tabla")
