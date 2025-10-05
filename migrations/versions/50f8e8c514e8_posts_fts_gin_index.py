"""posts FTS GIN index

Revision ID: 50f8e8c514e8
Revises: fb5a8b6a5f6f
Create Date: 2025-10-05 13:45:30.235719

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "50f8e8c514e8"
down_revision: Union[str, Sequence[str], None] = "fb5a8b6a5f6f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    CREATE INDEX IF NOT EXISTS ix_posts_fts
    ON posts
    USING GIN (
      to_tsvector(
        'simple',
        coalesce(title,'') || ' ' || coalesce(content,'')
      )
    );
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_posts_fts;")
