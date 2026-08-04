from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearRecibo(BaseModel):
    condominio_id: Optional[int] = None
    factura_id: Optional[int] = None
    unidad_id: Optional[int] = None
    propietario_id: Optional[int] = None
    subtotal: Optional[float] = 0
    total: Optional[float] = 0
    mora: Optional[float] = 0


class SolicitudActualizarRecibo(BaseModel):
    subtotal: Optional[float] = None
    mora: Optional[float] = None
    total: Optional[float] = None
    estado: Optional[str] = None


class RespuestaRecibo(BaseModel):
    id: int
    condominio_id: Optional[int] = None
    factura_id: Optional[int] = None
    unidad_id: Optional[int] = None
    propietario_id: Optional[int] = None
    subtotal: float
    mora: float
    total: float
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaRecibos(BaseModel):
    items: List[RespuestaRecibo]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
