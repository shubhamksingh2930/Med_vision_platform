"""add error_message to prediction_records
Revision ID: 0210e94d059c
Revises: d03355e19c6b
Create Date: 2026-08-09 19:16:12.672034
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0210e94d059c'
down_revision: Union[str, Sequence[str], None] = 'd03355e19c6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('prediction_records', sa.Column('error_message', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('prediction_records', 'error_message')