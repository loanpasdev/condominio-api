"""agregar_logo_condominios

Revision ID: a1b2c3d4e5f6
Revises: d60e45f2e78e
Create Date: 2026-07-17 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = 'd60e45f2e78e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('condominios', sa.Column('logo', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('condominios', 'logo')
