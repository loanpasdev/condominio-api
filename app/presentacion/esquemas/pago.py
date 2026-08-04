from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SolicitudCrearPago(BaseModel):
    condominio_id: Optional[int] = None
    cuota_id: Optional[int] = None
    propietario_id: Optional[int] = None
    monto: float
    metodo_pago_id: Optional[int] = None
    moneda_id: Optional[int] = None
    fecha_pago: Optional[datetime] = None
    referencia: Optional[str] = None
    notas: Optional[str] = None


class SolicitudActualizarPago(BaseModel):
    monto: Optional[float] = None
    metodo_pago_id: Optional[int] = None
    moneda_id: Optional[int] = None
    referencia: Optional[str] = None
    fecha_pago: Optional[datetime] = None
    notas: Optional[str] = None
    estado: Optional[str] = None


class RespuestaPago(BaseModel):
    id: int
    condominio_id: Optional[int] = None
    cuota_id: Optional[int] = None
    propietario_id: Optional[int] = None
    monto: float
    metodo_pago_id: Optional[int] = None
    moneda_id: Optional[int] = None
    referencia: Optional[str] = None
    fecha_pago: datetime
    notas: Optional[str] = None
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaPagos(BaseModel):
    items: List[RespuestaPago]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
