"""add content-hash column

Revision ID: 46c4949fc047
Revises: 921c01669bba
Create Date: 2026-08-26 15:01:27.525410
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "46c4949fc047"
down_revision: Union[str, Sequence[str], None] = "921c01669bba"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column(
        "documents",
        sa.Column(
            "content_hash",
            sa.String(64),
            nullable=False,
        ),
    )

    op.create_unique_constraint(
        "uq_documents_content_hash",
        "documents",
        ["content_hash"],
    )


def downgrade() -> None:

    op.drop_constraint(
        "uq_documents_content_hash",
        "documents",
        type_="unique",
    )

    op.drop_column(
        "documents",
        "content_hash",
    )