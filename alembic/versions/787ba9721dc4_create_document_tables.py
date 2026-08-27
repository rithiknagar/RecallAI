"""create document tables

Revision ID: 921c01669bba
Revises: 
Create Date: 2026-08-26 14:27:05.668249

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '921c01669bba'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


def upgrade() -> None:

    op.execute(
        "CREATE EXTENSION IF NOT EXISTS vector"
    )

    op.create_table(
        "documents",

        sa.Column(
            "id",
            sa.UUID(),
            primary_key=True,
        ),

        sa.Column(
            "filename",
            sa.String(500),
            nullable=False,
        ),

        sa.Column(
            "title",
            sa.String(500),
            nullable=True,
        ),

        sa.Column(
            "document_type",
            sa.String(100),
            nullable=True,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_table(
        "document_chunks",

        sa.Column(
            "id",
            sa.UUID(),
            primary_key=True,
        ),

        sa.Column(
            "document_id",
            sa.UUID(),
            sa.ForeignKey(
                "documents.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),

        sa.Column(
            "chunk_index",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "content",
            sa.Text(),
            nullable=False,
        ),

        sa.Column(
            "metadata",
            sa.JSON(),
            nullable=False,
        ),

        sa.Column(
            "embedding",
            Vector(384),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index(
        "document_chunks_document_id_idx",
        "document_chunks",
        ["document_id"],
    )

    op.execute(
        """
        CREATE INDEX document_chunks_embedding_hnsw_idx
        ON document_chunks
        USING hnsw (embedding vector_cosine_ops)
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
