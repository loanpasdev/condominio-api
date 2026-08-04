from pydantic import BaseModel
from typing import List


class SolicitudCrearBanco(BaseModel):
    codigo: str
    nombre: str


class SolicitudActualizarBanco(BaseModel):
    codigo: str
    nombre: str


class RespuestaBanco(BaseModel):
    id: int
    codigo: str
    nombre: str

    class Config:
        from_attributes = True


class RespuestaListaBancos(BaseModel):
    items: List[RespuestaBanco]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
