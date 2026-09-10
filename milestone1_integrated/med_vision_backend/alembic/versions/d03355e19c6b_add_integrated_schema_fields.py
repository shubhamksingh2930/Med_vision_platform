"""Add integrated schema fields

Revision ID: d03355e19c6b
Revises: 01ca52f18921
Create Date: 2026-07-25 23:30:15.042082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd03355e19c6b'
down_revision: Union[str, Sequence[str], None] = '01ca52f18921'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass