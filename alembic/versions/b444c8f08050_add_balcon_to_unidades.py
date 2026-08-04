"""add_balcon_to_unidades

Revision ID: b444c8f08050
Revises: g1h2i3j4k5l6
Create Date: 2026-07-18 00:21:39.574851

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b444c8f08050'
down_revision: Union[str, None] = 'g1h2i3j4k5l6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('unidades', sa.Column('balcon', sa.Boolean(), server_default=sa.text('false'), nullable=True))


def downgrade() -> None:
    op.drop_column('unidades', 'balcon')
