"""Crear tabla propietarios

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-07-17

"""
from alembic import op
import sqlalchemy as sa


revision = 'f6a7b8c9d0e1'
down_revision = 'e5f6a7b8c9d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'propietarios',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('nombre', sa.String(100), nullable=False),
        sa.Column('apellido', sa.String(100), nullable=False),
        sa.Column('cedula', sa.String(20), nullable=False),
        sa.Column('correo', sa.String(100), nullable=False),
        sa.Column('telefono', sa.String(20), nullable=True),
        sa.Column('direccion', sa.String(200), nullable=True),
        sa.Column('tipo_unidad_id', sa.Integer(), sa.ForeignKey('tipos_unidad.id'), nullable=True),
        sa.Column('unidad_numero', sa.String(20), nullable=True),
        sa.Column('estado', sa.String(20), server_default='activo'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('propietarios')
