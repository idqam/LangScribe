"""change language enum

Revision ID: f7ca6f9f5035
Revises: d04863a598b5
Create Date: 2025-11-17 11:29:49.634847

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f7ca6f9f5035'
down_revision: Union[str, Sequence[str], None] = 'd04863a598b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade():
    # 1. Create NEW enum type
    op.execute("CREATE TYPE code_new AS ENUM ('en', 'es')")
    op.execute("ALTER TABLE languages ALTER COLUMN code TYPE TEXT")
    op.execute("DROP TYPE code")
    op.execute("ALTER TYPE code_new RENAME TO code")
    op.execute("ALTER TABLE languages ALTER COLUMN code TYPE code USING code::code")

    op.execute("""
        ALTER TABLE languages
        ALTER COLUMN difficulty TYPE INTEGER
        USING difficulty::integer
    """)

def downgrade() -> None:
    """Downgrade schema."""
    pass
