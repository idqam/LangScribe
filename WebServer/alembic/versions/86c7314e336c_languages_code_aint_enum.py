"""languages code aint enum

Revision ID: 86c7314e336c
Revises: f7ca6f9f5035
Create Date: 2025-11-20 08:55:29.091878

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86c7314e336c'
down_revision: Union[str, Sequence[str], None] = 'f7ca6f9f5035'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('languages','code')
    op.add_column(
        'languages',
        sa.Column('code_short', sa.String(length=2), nullable=True)
    )
    op.create_unique_constraint(
        'uq_languages_code_short',
        'languages',
        ['code_short']
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
