from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class SolicitudCrearFactura(BaseModel):
    condominio_id: int
    numero: str
    descripcion: str
    monto_total: float
    fecha: date
    distribucion: str
    destino_id: Optional[int] = None


class SolicitudActualizarFactura(BaseModel):
    numero: str
    descripcion: str
    monto_total: float
    fecha: date
    distribucion: str
    destino_id: Optional[int] = None
    estado: str = "pendiente"


class RespuestaFactura(BaseModel):
    id: int
    condominio_id: int
    numero: str
    descripcion: str
    monto_total: float
    fecha: date
    distribucion: str
    destino_id: Optional[int] = None
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaFacturas(BaseModel):
    items: List[RespuestaFactura]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
