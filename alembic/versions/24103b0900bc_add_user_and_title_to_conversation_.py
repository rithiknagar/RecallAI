"""add user and title to conversation sessions

Revision ID: 24103b0900bc
Revises: 64d50717f2c9
Create Date: 2026-09-02 11:47:58.470206
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = '24103b0900bc'
down_revision: Union[str, Sequence[str], None] = '64d50717f2c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "conversation_sessions",
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
    )

    op.add_column(
        "conversation_sessions",
        sa.Column(
            "title",
            sa.String(length=255),
            nullable=False,
            server_default="New Conversation",
        ),
    )

    op.create_index(
        "ix_conversation_sessions_user_id",
        "conversation_sessions",
        ["user_id"],
        unique=False,
    )

    op.create_foreign_key(
        "fk_conversation_sessions_user_id_users",
        "conversation_sessions",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:

    op.drop_constraint(
        "fk_conversation_sessions_user_id_users",
        "conversation_sessions",
        type_="foreignkey",
    )

    op.drop_index(
        "ix_conversation_sessions_user_id",
        table_name="conversation_sessions",
    )

    op.drop_column(
        "conversation_sessions",
        "title",
    )

    op.drop_column(
        "conversation_sessions",
        "user_id",
    )
