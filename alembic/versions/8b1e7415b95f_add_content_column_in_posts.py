"""add content column in posts

Revision ID: 8b1e7415b95f
Revises: 5e7b174d5b2d
Create Date: 2026-03-19 16:10:43.149291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b1e7415b95f'
down_revision: Union[str, Sequence[str], None] = '5e7b174d5b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
