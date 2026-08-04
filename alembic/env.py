from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
import sys

# Agregar el directorio raiz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.database import Base
from app.config import configuracion

# Importar todos los modelos para que Alembic los detecte
from app.infraestructura.modelado import modelo_usuario
from app.infraestructura.modelado import modelo_condominio
from app.infraestructura.modelado import modelo_tipo_unidad
from app.infraestructura.modelado import modelo_banco
from app.infraestructura.modelado import modelo_tipo_cuenta_bancaria
from app.infraestructura.modelado import modelo_metodo_pago
from app.infraestructura.modelado import modelo_moneda
from app.infraestructura.modelado import modelo_proveedor
from app.infraestructura.modelado import modelo_categoria_gasto
from app.infraestructura.modelado import modelo_plan_cuenta
from app.infraestructura.modelado import modelo_area_comun
from app.infraestructura.modelado import modelo_modulo
from app.infraestructura.modelado import modelo_rol_modulo

config = context.config
config.set_main_option("sqlalchemy.url", configuracion.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
