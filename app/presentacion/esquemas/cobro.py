from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class SolicitudCrearCobro(BaseModel):
    condominio_id: Optional[int] = None
    categoria_id: Optional[int] = None
    descripcion: str = ""
    monto: float = 0
    fecha: Optional[date] = None
    proveedor_id: Optional[int] = None


class SolicitudActualizarCobro(BaseModel):
    categoria_id: Optional[int] = None
    descripcion: Optional[str] = None
    monto: Optional[float] = None
    fecha: Optional[date] = None
    proveedor_id: Optional[int] = None


class RespuestaCobro(BaseModel):
    id: int
    condominio_id: Optional[int] = None
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    descripcion: str
    monto: float
    fecha: date

    class Config:
        from_attributes = True


class RespuestaListaCobros(BaseModel):
    items: List[RespuestaCobro]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
