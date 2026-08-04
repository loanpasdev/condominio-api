"""alter unidades and propietarios

Revision ID: g1h2i3j4k5l6
Revises: f6a7b8c9d0e1
Create Date: 2026-07-17
"""
from alembic import op
import sqlalchemy as sa

revision = 'g1h2i3j4k5l6'
down_revision = 'f6a7b8c9d0e1'
branch_labels = None
depends_on = None


def upgrade():
    # Unidades: add new columns
    op.add_column('unidades', sa.Column('grupo', sa.String(50), nullable=True))
    op.add_column('unidades', sa.Column('habitaciones', sa.Integer(), server_default='0'))
    op.add_column('unidades', sa.Column('banios', sa.Integer(), server_default='0'))
    op.add_column('unidades', sa.Column('terraza', sa.Boolean(), server_default='false'))
    op.add_column('unidades', sa.Column('parking', sa.Boolean(), server_default='false'))
    op.add_column('unidades', sa.Column('notas', sa.String(500), nullable=True))

    # Unidades: fix FK propietario_id from usuarios to propietarios
    op.drop_constraint('unidades_propietario_id_fkey', 'unidades', type_='foreignkey')
    op.create_foreign_key('unidades_propietario_id_fkey', 'unidades', 'propietarios', ['propietario_id'], ['id'])

    # Propietarios: drop redundant columns
    op.drop_constraint('propietarios_tipo_unidad_id_fkey', 'propietarios', type_='foreignkey')
    op.drop_column('propietarios', 'tipo_unidad_id')
    op.drop_column('propietarios', 'unidad_numero')


def downgrade():
    op.add_column('propietarios', sa.Column('unidad_numero', sa.String(20), nullable=True))
    op.add_column('propietarios', sa.Column('tipo_unidad_id', sa.Integer(), nullable=True))
    op.create_foreign_key('propietarios_tipo_unidad_id_fkey', 'propietarios', 'tipos_unidad', ['tipo_unidad_id'], ['id'])

    op.drop_constraint('unidades_propietario_id_fkey', 'unidades', type_='foreignkey')
    op.create_foreign_key('unidades_propietario_id_fkey', 'unidades', 'usuarios', ['propietario_id'], ['id'])

    op.drop_column('unidades', 'notas')
    op.drop_column('unidades', 'parking')
    op.drop_column('unidades', 'terraza')
    op.drop_column('unidades', 'banios')
    op.drop_column('unidades', 'habitaciones')
    op.drop_column('unidades', 'grupo')
