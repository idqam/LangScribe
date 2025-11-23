"""relations now cascade

Revision ID: 30bc98dd9245
Revises: 86c7314e336c
Create Date: 2025-11-21 08:33:08.000164

"""
from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "30bc98dd9245"
down_revision: str | Sequence[str] | None = "86c7314e336c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("prompts_language_id_fkey", "prompts", type_="foreignkey")
    op.create_foreign_key(
        "prompts_language_id_fkey",
        "prompts",
        "languages",
        ["language_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Drop and recreate foreign key for reports table
    op.drop_constraint("reports_language_id_fkey", "reports", type_="foreignkey")
    op.create_foreign_key(
        "reports_language_id_fkey",
        "reports",
        "languages",
        ["language_id"],
        ["id"],
        ondelete="CASCADE",

    )

    # Drop and recreate foreign key for user_languages table
    op.drop_constraint("user_languages_language_id_fkey", "user_languages", type_="foreignkey")
    op.create_foreign_key(
        "user_languages_language_id_fkey",
        "user_languages",
        "languages",
        ["language_id"],
        ["id"],
        ondelete="CASCADE",
    )

    op.drop_constraint("reports_user_id_fkey", "reports", type_="foreignkey")
    op.create_foreign_key(
        "reports_user_id_fkey",
        "reports",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Drop and recreate foreign key for user_languages table
    op.drop_constraint("user_languages_user_id_fkey", "user_languages", type_="foreignkey")
    op.create_foreign_key(
        "user_languages_user_id_fkey",
        "user_languages",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )

    # Drop and recreate foreign key for user_messages table
    op.drop_constraint("user_messages_user_id_fkey", "user_messages", type_="foreignkey")
    op.create_foreign_key(
        "user_messages_user_id_fkey",
        "user_messages",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("user_messages_user_id_fkey", "user_messages", type_="foreignkey")
    op.create_foreign_key(
        "user_messages_user_id_fkey",
        "user_messages",
        "users",
        ["user_id"],
        ["id"],
    )

    # Revert foreign key for user_languages table (without CASCADE)
    op.drop_constraint("user_languages_user_id_fkey", "user_languages", type_="foreignkey")
    op.create_foreign_key(
        "user_languages_user_id_fkey",
        "user_languages",
        "users",
        ["user_id"],
        ["id"],
    )

    # Revert foreign key for reports table (without CASCADE)
    op.drop_constraint("reports_user_id_fkey", "reports", type_="foreignkey")
    op.create_foreign_key(
        "reports_user_id_fkey",
        "reports",
        "users",
        ["user_id"],
        ["id"],
    )

    op.drop_constraint("user_languages_language_id_fkey", "user_languages", type_="foreignkey")
    op.create_foreign_key(
        "user_languages_language_id_fkey",
        "user_languages",
        "languages",
        ["language_id"],
        ["id"],
    )

    # Revert foreign key for reports table (without CASCADE)
    op.drop_constraint("reports_language_id_fkey", "reports", type_="foreignkey")
    op.create_foreign_key(
        "reports_language_id_fkey",
        "reports",
        "languages",
        ["language_id"],
        ["id"],
    )

    # Revert foreign key for prompts table (without CASCADE)
    op.drop_constraint("prompts_language_id_fkey", "prompts", type_="foreignkey")
    op.create_foreign_key(
        "prompts_language_id_fkey",
        "prompts",
        "languages",
        ["language_id"],
        ["id"],
    )
