from pydantic import BaseModel
from typing import List


class SolicitudCrearMetodoPago(BaseModel):
    nombre: str
    condominio_id: int


class SolicitudActualizarMetodoPago(BaseModel):
    nombre: str
    condominio_id: int
    estado: str = "activo"


class RespuestaMetodoPago(BaseModel):
    id: int
    nombre: str
    condominio_id: int
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaMetodosPago(BaseModel):
    items: List[RespuestaMetodoPago]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
