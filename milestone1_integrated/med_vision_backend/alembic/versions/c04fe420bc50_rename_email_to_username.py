"""rename email to username

Revision ID: c04fe420bc50
Revises: 0210e94d059c
Create Date: 2026-09-30 06:43:57.967539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c04fe420bc50'
down_revision: Union[str, Sequence[str], None] = '0210e94d059c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.alter_column('users', 'email', new_column_name='username')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.alter_column('users', 'username', new_column_name='email')
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
