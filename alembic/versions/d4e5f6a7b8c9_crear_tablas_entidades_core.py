"""Crear tablas de entidades core: unidades, cuotas, pagos, cobros, solicitudes, reservas, notificaciones, cuentas_bancarias, facturas, recibos, asambleas

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-07-17

"""
from alembic import op
import sqlalchemy as sa


revision = 'd4e5f6a7b8c9'
down_revision = 'c3d4e5f6a7b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Unidades
    op.create_table(
        'unidades',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('tipo_unidad_id', sa.Integer(), sa.ForeignKey('tipos_unidad.id'), nullable=False),
        sa.Column('propietario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('numero', sa.String(10), nullable=False),
        sa.Column('piso', sa.Integer()),
        sa.Column('metraje', sa.Numeric(8, 2), nullable=False),
        sa.Column('porcentual', sa.Numeric(5, 2), nullable=False),
        sa.Column('estado', sa.String(20), server_default='activo'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint('condominio_id', 'numero', name='uq_unidad_condominio_numero'),
    )

    # Cuotas
    op.create_table(
        'cuotas',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('unidad_id', sa.Integer(), sa.ForeignKey('unidades.id'), nullable=False),
        sa.Column('mes', sa.Integer(), nullable=False),
        sa.Column('anio', sa.Integer(), nullable=False),
        sa.Column('monto_total', sa.Numeric(10, 2), nullable=False),
        sa.Column('estado', sa.String(20), server_default='pendiente'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
        sa.UniqueConstraint('unidad_id', 'mes', 'anio', name='uq_cuota_unidad_periodo'),
    )

    # Pagos
    op.create_table(
        'pagos',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('cuota_id', sa.Integer(), sa.ForeignKey('cuotas.id'), nullable=False),
        sa.Column('propietario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('monto', sa.Numeric(10, 2), nullable=False),
        sa.Column('metodo_pago_id', sa.Integer(), sa.ForeignKey('metodos_pago.id'), nullable=False),
        sa.Column('moneda_id', sa.Integer(), sa.ForeignKey('monedas.id'), nullable=False),
        sa.Column('referencia', sa.String(100)),
        sa.Column('fecha_pago', sa.DateTime(), nullable=False),
        sa.Column('notas', sa.Text()),
        sa.Column('estado', sa.String(20), server_default='completado'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
    )

    # Cobros
    op.create_table(
        'cobros',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('categoria_id', sa.Integer(), sa.ForeignKey('categorias_gasto.id'), nullable=False),
        sa.Column('proveedor_id', sa.Integer(), sa.ForeignKey('proveedores.id'), nullable=True),
        sa.Column('descripcion', sa.Text(), nullable=False),
        sa.Column('monto', sa.Numeric(10, 2), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
    )

    # Solicitudes
    op.create_table(
        'solicitudes',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('propietario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('titulo', sa.String(200), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=False),
        sa.Column('categoria', sa.String(50), nullable=False),
        sa.Column('prioridad', sa.String(20), server_default='media'),
        sa.Column('estado', sa.String(20), server_default='abierta'),
        sa.Column('responsable', sa.String(100)),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
    )

    # Reservas
    op.create_table(
        'reservas',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('area_comun_id', sa.Integer(), sa.ForeignKey('areas_comunes.id'), nullable=False),
        sa.Column('propietario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('hora_inicio', sa.Time(), nullable=False),
        sa.Column('hora_fin', sa.Time(), nullable=False),
        sa.Column('estado', sa.String(20), server_default='confirmada'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
    )

    # Notificaciones
    op.create_table(
        'notificaciones',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('usuario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=True),
        sa.Column('titulo', sa.String(200), nullable=False),
        sa.Column('mensaje', sa.Text(), nullable=False),
        sa.Column('tipo', sa.String(50), nullable=False),
        sa.Column('leida', sa.Boolean(), server_default='false'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
    )

    # Cuentas Bancarias
    op.create_table(
        'cuentas_bancarias',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('banco_id', sa.Integer(), sa.ForeignKey('bancos.id'), nullable=False),
        sa.Column('tipo_cuenta_id', sa.Integer(), sa.ForeignKey('tipos_cuenta_bancaria.id'), nullable=False),
        sa.Column('numero_cuenta', sa.String(30), nullable=False),
        sa.Column('titular', sa.String(100), nullable=False),
        sa.Column('moneda_id', sa.Integer(), sa.ForeignKey('monedas.id'), nullable=False),
        sa.Column('saldo', sa.Numeric(12, 2), server_default='0'),
        sa.Column('estado', sa.String(20), server_default='activo'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
    )

    # Facturas
    op.create_table(
        'facturas',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('numero', sa.String(20), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=False),
        sa.Column('monto_total', sa.Numeric(10, 2), nullable=False),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('distribucion', sa.String(20), nullable=False),
        sa.Column('destino_id', sa.Integer()),
        sa.Column('estado', sa.String(20), server_default='pendiente'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
    )

    # Recibos
    op.create_table(
        'recibos',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('factura_id', sa.Integer(), sa.ForeignKey('facturas.id'), nullable=False),
        sa.Column('unidad_id', sa.Integer(), sa.ForeignKey('unidades.id'), nullable=False),
        sa.Column('propietario_id', sa.Integer(), sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('subtotal', sa.Numeric(10, 2), nullable=False),
        sa.Column('mora', sa.Numeric(10, 2), server_default='0'),
        sa.Column('total', sa.Numeric(10, 2), nullable=False),
        sa.Column('estado', sa.String(20), server_default='pendiente'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
    )

    # Asambleas
    op.create_table(
        'asambleas',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('condominio_id', sa.Integer(), sa.ForeignKey('condominios.id'), nullable=False),
        sa.Column('tipo', sa.String(20), nullable=False),
        sa.Column('titulo', sa.String(200), nullable=False),
        sa.Column('descripcion', sa.Text()),
        sa.Column('fecha', sa.Date(), nullable=False),
        sa.Column('hora', sa.Time(), nullable=False),
        sa.Column('lugar', sa.String(200)),
        sa.Column('quorum_requerido', sa.Numeric(5, 2), nullable=False),
        sa.Column('quorum_obtenido', sa.Numeric(5, 2), server_default='0'),
        sa.Column('estado', sa.String(20), server_default='programada'),
        sa.Column('fecha_creacion', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('fecha_actualizacion', sa.DateTime(), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table('asambleas')
    op.drop_table('recibos')
    op.drop_table('facturas')
    op.drop_table('cuentas_bancarias')
    op.drop_table('notificaciones')
    op.drop_table('reservas')
    op.drop_table('solicitudes')
    op.drop_table('cobros')
    op.drop_table('pagos')
    op.drop_table('cuotas')
    op.drop_table('unidades')
