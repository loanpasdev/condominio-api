from pydantic import BaseModel
from typing import List


class SolicitudCrearCategoriaGasto(BaseModel):
    nombre: str
    condominio_id: int


class SolicitudActualizarCategoriaGasto(BaseModel):
    nombre: str
    condominio_id: int
    estado: str = "activo"


class RespuestaCategoriaGasto(BaseModel):
    id: int
    nombre: str
    condominio_id: int
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaCategoriasGasto(BaseModel):
    items: List[RespuestaCategoriaGasto]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
