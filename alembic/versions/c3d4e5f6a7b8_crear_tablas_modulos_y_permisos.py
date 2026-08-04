"""crear_tablas_modulos_y_permisos

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-07-17 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'modulos',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('codigo', sa.String(50), unique=True, nullable=False),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
    )

    op.create_table(
        'rol_modulo',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('rol', sa.String(20), nullable=False),
        sa.Column('modulo_id', sa.Integer(), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
    )

    modulos_tabla = sa.table('modulos',
        sa.column('id', sa.Integer),
        sa.column('codigo', sa.String),
        sa.column('nombre', sa.String),
    )

    op.bulk_insert(modulos_tabla, [
        {'id': 1, 'codigo': 'dashboard', 'nombre': 'Dashboard'},
        {'id': 2, 'codigo': 'reportes', 'nombre': 'Reportes'},
        {'id': 3, 'codigo': 'notificaciones', 'nombre': 'Notificaciones'},
        {'id': 4, 'codigo': 'propietarios', 'nombre': 'Propietarios'},
        {'id': 5, 'codigo': 'unidades', 'nombre': 'Unidades'},
        {'id': 6, 'codigo': 'pagos', 'nombre': 'Pagos'},
        {'id': 7, 'codigo': 'cuotas', 'nombre': 'Cuotas'},
        {'id': 8, 'codigo': 'morosos', 'nombre': 'Morosos'},
        {'id': 9, 'codigo': 'cobros', 'nombre': 'Cobros'},
        {'id': 10, 'codigo': 'categorias', 'nombre': 'Categorias'},
        {'id': 11, 'codigo': 'conciliacion', 'nombre': 'Conciliacion'},
        {'id': 12, 'codigo': 'proveedores', 'nombre': 'Proveedores'},
        {'id': 13, 'codigo': 'solicitudes', 'nombre': 'Solicitudes'},
        {'id': 14, 'codigo': 'reservas', 'nombre': 'Reservas'},
        {'id': 15, 'codigo': 'amenidades', 'nombre': 'Areas Comunes'},
        {'id': 16, 'codigo': 'finanzas', 'nombre': 'Finanzas'},
        {'id': 17, 'codigo': 'contabilidad', 'nombre': 'Contabilidad'},
        {'id': 18, 'codigo': 'configuracion', 'nombre': 'Configuracion'},
        {'id': 19, 'codigo': 'usuarios', 'nombre': 'Usuarios'},
    ])

    permisos_tabla = sa.table('rol_modulo',
        sa.column('rol', sa.String),
        sa.column('modulo_id', sa.Integer),
    )

    op.bulk_insert(permisos_tabla, [
        # Admin: todo
        {'rol': 'admin', 'modulo_id': 1},
        {'rol': 'admin', 'modulo_id': 2},
        {'rol': 'admin', 'modulo_id': 3},
        {'rol': 'admin', 'modulo_id': 4},
        {'rol': 'admin', 'modulo_id': 5},
        {'rol': 'admin', 'modulo_id': 6},
        {'rol': 'admin', 'modulo_id': 7},
        {'rol': 'admin', 'modulo_id': 8},
        {'rol': 'admin', 'modulo_id': 9},
        {'rol': 'admin', 'modulo_id': 10},
        {'rol': 'admin', 'modulo_id': 11},
        {'rol': 'admin', 'modulo_id': 12},
        {'rol': 'admin', 'modulo_id': 13},
        {'rol': 'admin', 'modulo_id': 14},
        {'rol': 'admin', 'modulo_id': 15},
        {'rol': 'admin', 'modulo_id': 16},
        {'rol': 'admin', 'modulo_id': 17},
        {'rol': 'admin', 'modulo_id': 18},
        {'rol': 'admin', 'modulo_id': 19},
        # Tesorera: finanzas, cobros, pagos, cuotas, etc.
        {'rol': 'tesorera', 'modulo_id': 1},
        {'rol': 'tesorera', 'modulo_id': 2},
        {'rol': 'tesorera', 'modulo_id': 3},
        {'rol': 'tesorera', 'modulo_id': 4},
        {'rol': 'tesorera', 'modulo_id': 5},
        {'rol': 'tesorera', 'modulo_id': 6},
        {'rol': 'tesorera', 'modulo_id': 7},
        {'rol': 'tesorera', 'modulo_id': 8},
        {'rol': 'tesorera', 'modulo_id': 9},
        {'rol': 'tesorera', 'modulo_id': 10},
        {'rol': 'tesorera', 'modulo_id': 11},
        {'rol': 'tesorera', 'modulo_id': 12},
        {'rol': 'tesorera', 'modulo_id': 13},
        {'rol': 'tesorera', 'modulo_id': 14},
        {'rol': 'tesorera', 'modulo_id': 15},
        {'rol': 'tesorera', 'modulo_id': 16},
        {'rol': 'tesorera', 'modulo_id': 17},
        # Secretario: gestion, propietarios, unidades, solicitudes
        {'rol': 'secretario', 'modulo_id': 1},
        {'rol': 'secretario', 'modulo_id': 2},
        {'rol': 'secretario', 'modulo_id': 3},
        {'rol': 'secretario', 'modulo_id': 4},
        {'rol': 'secretario', 'modulo_id': 5},
        {'rol': 'secretario', 'modulo_id': 12},
        {'rol': 'secretario', 'modulo_id': 13},
        {'rol': 'secretario', 'modulo_id': 14},
        {'rol': 'secretario', 'modulo_id': 15},
        # Consejo: reportes, notificaciones, solicitudes, reservas
        {'rol': 'consejo', 'modulo_id': 1},
        {'rol': 'consejo', 'modulo_id': 2},
        {'rol': 'consejo', 'modulo_id': 3},
        {'rol': 'consejo', 'modulo_id': 13},
        {'rol': 'consejo', 'modulo_id': 14},
        # Propietario: basico
        {'rol': 'propietario', 'modulo_id': 1},
        {'rol': 'propietario', 'modulo_id': 3},
        {'rol': 'propietario', 'modulo_id': 13},
        {'rol': 'propietario', 'modulo_id': 14},
    ])


def downgrade() -> None:
    op.drop_table('rol_modulo')
    op.drop_table('modulos')
