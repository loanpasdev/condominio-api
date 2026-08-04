from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearTipoUnidad(BaseModel):
    nombre: str
    condominio_id: int


class SolicitudActualizarTipoUnidad(BaseModel):
    nombre: str
    condominio_id: int
    estado: str = "activo"


class RespuestaTipoUnidad(BaseModel):
    id: int
    nombre: str
    condominio_id: int
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaTiposUnidad(BaseModel):
    items: List[RespuestaTipoUnidad]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
