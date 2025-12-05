"""user native/default language

Revision ID: 8a81258deb85
Revises: 2cad4cfcd2f1
Create Date: 2025-12-05 08:26:48.174270

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a81258deb85'
down_revision: Union[str, Sequence[str], None] = '2cad4cfcd2f1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column('default_language', sa.String, nullable = True)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'users',
        'default_language'
    )
