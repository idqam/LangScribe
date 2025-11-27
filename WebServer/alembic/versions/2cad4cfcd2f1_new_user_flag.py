"""new user flag

Revision ID: 2cad4cfcd2f1
Revises: 30bc98dd9245
Create Date: 2025-11-27 08:01:40.664697

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2cad4cfcd2f1'
down_revision: Union[str, Sequence[str], None] = '30bc98dd9245'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'new_user',
            sa.Boolean(),
            nullable=False,
            server_default=sa.text('false'),
        )
    )
    
    op.add_column(
        'user_languages',
        sa.Column(
            "desired_level",
            sa.Enum("A1", "A2", "B1", "B2", "C1", "C2", name="proficiency_levels"),
            nullable=False,
            server_default=sa.text("'A1'")
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        'users',
        'new_user'
    )
    op.drop_column(
        'user_languages',
        'desired_level'
    )
