"""convert_estado_to_boolean

Revision ID: 6ac266c6bdf2
Revises: b444c8f08050
Create Date: 2026-07-18 01:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6ac266c6bdf2'
down_revision: Union[str, None] = 'b444c8f08050'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    for tabla in ['unidades', 'propietarios', 'grupos_residenciales']:
        op.execute(f"UPDATE {tabla} SET estado = 'true' WHERE estado = 'activo' OR estado IS NULL")
        op.execute(f"UPDATE {tabla} SET estado = 'false' WHERE estado = 'inactivo' OR estado = ''")
        op.execute(f"ALTER TABLE {tabla} ALTER COLUMN estado DROP DEFAULT")
        op.execute(f"ALTER TABLE {tabla} ALTER COLUMN estado TYPE BOOLEAN USING estado::boolean")
        op.execute(f"ALTER TABLE {tabla} ALTER COLUMN estado SET DEFAULT true")
        op.execute(f"ALTER TABLE {tabla} ALTER COLUMN estado SET NOT NULL")


def downgrade() -> None:
    for tabla in ['unidades', 'propietarios', 'grupos_residenciales']:
        op.execute(f"ALTER TABLE {tabla} ALTER COLUMN estado DROP DEFAULT")
        op.execute(f"ALTER TABLE {tabla} ALTER COLUMN estado TYPE VARCHAR(20) USING CASE WHEN estado THEN 'activo' ELSE 'inactivo' END")
        op.execute(f"ALTER TABLE {tabla} ALTER COLUMN estado SET DEFAULT 'activo'")
