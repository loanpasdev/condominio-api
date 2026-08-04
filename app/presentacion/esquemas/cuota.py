from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearCuota(BaseModel):
    condominio_id: Optional[int] = None
    unidad_id: Optional[int] = None
    mes: Optional[int] = None
    anio: Optional[int] = None
    monto_total: float = 0


class SolicitudActualizarCuota(BaseModel):
    monto_total: Optional[float] = None
    estado: Optional[str] = None


class RespuestaCuota(BaseModel):
    id: int
    condominio_id: Optional[int] = None
    unidad_id: Optional[int] = None
    mes: int
    anio: int
    monto_total: float
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaCuotas(BaseModel):
    items: List[RespuestaCuota]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
