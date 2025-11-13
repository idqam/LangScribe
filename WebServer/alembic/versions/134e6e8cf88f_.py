"""Revision ID: 134e6e8cf88f
Revises: dcca8e27d7db
Create Date: 2025-11-11 19:49:25.981937

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "134e6e8cf88f"
down_revision: str | Sequence[str] | None = "dcca8e27d7db"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""


def downgrade() -> None:
    """Downgrade schema."""
