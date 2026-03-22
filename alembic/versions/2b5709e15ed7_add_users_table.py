"""add users table

Revision ID: 2b5709e15ed7
Revises: 8b1e7415b95f
Create Date: 2026-03-19 16:20:12.299174

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b5709e15ed7'
down_revision: Union[str, Sequence[str], None] = '8b1e7415b95f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', sa.Column('id', sa.Integer, primary_key=True, nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    sa.UniqueConstraint("email"))
    pass

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')
    pass
