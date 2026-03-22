"""add fk in post

Revision ID: 298fb47262ee
Revises: 2b5709e15ed7
Create Date: 2026-03-19 16:45:38.782117

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '298fb47262ee'
down_revision: Union[str, Sequence[str], None] = '2b5709e15ed7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_user_fk", source_table="posts", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass

def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
