"""seed_rol_modulo_presidente

Revision ID: h7k8l9m0n1o2
Revises: 6ac266c6bdf2
Create Date: 2026-07-18 10:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = 'h7k8l9m0n1o2'
down_revision: Union[str, None] = '6ac266c6bdf2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    permisos_tabla = sa.table('rol_modulo',
        sa.column('rol', sa.String),
        sa.column('modulo_id', sa.Integer),
    )

    modulos_tabla = sa.table('modulos',
        sa.column('id', sa.Integer),
        sa.column('codigo', sa.String),
    )

    # Obtener IDs de modulos existentes
    conn = op.get_bind()
    result = conn.execute(sa.select(modulos_tabla.c.id).order_by(modulos_tabla.c.id))
    modulo_ids = [row[0] for row in result]

    # Insertar permisos para presidente (todos los modulos)
    for modulo_id in modulo_ids:
        op.execute(
            permisos_tabla.insert().values(rol='presidente', modulo_id=modulo_id)
        )


def downgrade() -> None:
    op.execute("DELETE FROM rol_modulo WHERE rol = 'presidente'")
