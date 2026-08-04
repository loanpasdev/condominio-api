"""agregar_telefono_ultimo_acceso_usuarios

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-07-17 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('usuarios', sa.Column('telefono', sa.String(20), nullable=True))
    op.add_column('usuarios', sa.Column('ultimo_acceso', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('usuarios', 'ultimo_acceso')
    op.drop_column('usuarios', 'telefono')
