from fastapi import FastAPI
from app.database import engine, Base
from app.presentacion.middleware.cors import configurar_cors
from app.presentacion.rutas import (
    auth, usuarios, condominio, tipo_unidad, banco, tipo_cuenta_bancaria,
    metodo_pago, moneda, proveedor, categoria_gasto, plan_cuenta, area_comun,
    permisos, modulos, unidad, cuota, pago, cobro, solicitud, reserva, notificacion,
    cuenta_bancaria, factura, recibo, asamblea, propietario, grupo_residencial,
)

# Crear tablas faltantes (las existentes se ignoran)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Gestion de Condominios",
    description="API para administracion de condominios en Venezuela",
    version="3.0.0",
)

# Configurar middlewares
configurar_cors(app)

# Registrar rutas - Auth y Config
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(condominio.router)
app.include_router(permisos.router)
app.include_router(modulos.router)

# Registrar rutas - Datos Maestros
app.include_router(tipo_unidad.router)
app.include_router(banco.router)
app.include_router(tipo_cuenta_bancaria.router)
app.include_router(metodo_pago.router)
app.include_router(moneda.router)
app.include_router(proveedor.router)
app.include_router(categoria_gasto.router)
app.include_router(plan_cuenta.router)
app.include_router(area_comun.router)
app.include_router(grupo_residencial.router)

# Registrar rutas - Entidades Core
app.include_router(unidad.router)
app.include_router(cuota.router)
app.include_router(pago.router)
app.include_router(cobro.router)

# Registrar rutas - Operaciones
app.include_router(solicitud.router)
app.include_router(reserva.router)
app.include_router(notificacion.router)

# Registrar rutas - Finanzas
app.include_router(cuenta_bancaria.router)
app.include_router(factura.router)
app.include_router(recibo.router)

# Registrar rutas - Asambleas
app.include_router(asamblea.router)

# Registrar rutas - Propietarios
app.include_router(propietario.router)


@app.get("/")
def raiz():
    return {
        "mensaje": "Sistema de Gestion de Condominios API",
        "version": "3.0.0",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
