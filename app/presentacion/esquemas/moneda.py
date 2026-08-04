from pydantic import BaseModel
from typing import List, Optional


class SolicitudCrearMoneda(BaseModel):
    codigo: str
    nombre: str
    simbolo: str
    es_base: bool = False
    tasa_cambio: float = 1.0


class SolicitudActualizarMoneda(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    simbolo: Optional[str] = None
    estado: Optional[str] = None
    es_base: Optional[bool] = None
    tasa_cambio: Optional[float] = None


class RespuestaMoneda(BaseModel):
    id: int
    codigo: str
    nombre: str
    simbolo: str
    estado: str
    es_base: bool = False
    tasa_cambio: float = 1.0

    class Config:
        from_attributes = True


class RespuestaListaMonedas(BaseModel):
    items: List[RespuestaMoneda]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
