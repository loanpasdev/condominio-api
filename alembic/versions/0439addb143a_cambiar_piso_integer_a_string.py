"""cambiar_piso_integer_a_string

Revision ID: 0439addb143a
Revises: h7k8l9m0n1o2
Create Date: 2026-07-21 23:06:56.487241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = '0439addb143a'
down_revision: Union[str, None] = 'h7k8l9m0n1o2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('ALTER TABLE unidades ADD COLUMN piso_tmp VARCHAR(20)')
    op.execute('UPDATE unidades SET piso_tmp = piso::text WHERE piso IS NOT NULL')
    op.execute('ALTER TABLE unidades DROP COLUMN piso')
    op.execute('ALTER TABLE unidades RENAME COLUMN piso_tmp TO piso')


def downgrade() -> None:
    op.execute('ALTER TABLE unidades ADD COLUMN piso_tmp INTEGER')
    op.execute('UPDATE unidades SET piso_tmp = piso::integer WHERE piso IS NOT NULL')
    op.execute('ALTER TABLE unidades DROP COLUMN piso')
    op.execute('ALTER TABLE unidades RENAME COLUMN piso_tmp TO piso')
