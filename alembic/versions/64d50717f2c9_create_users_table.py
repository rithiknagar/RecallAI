"""create users table

Revision ID: 64d50717f2c9
Revises: 1e9fce526503
Create Date: 2026-09-02 11:39:05.237220
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = '64d50717f2c9'
down_revision: Union[str, Sequence[str], None] = '1e9fce526503'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.create_table(
        "users",

        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
        ),

        sa.Column(
            "email",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),

        sa.UniqueConstraint(
            "email",
            name="uq_users_email",
        ),
    )

    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=False,
    )


def downgrade() -> None:

    op.drop_index(
        "ix_users_email",
        table_name="users",
    )

    op.drop_table("users")
