from pydantic import BaseModel
from typing import List


class SolicitudCrearTipoCuentaBancaria(BaseModel):
    nombre: str
    condominio_id: int


class SolicitudActualizarTipoCuentaBancaria(BaseModel):
    nombre: str
    condominio_id: int
    estado: str = "activo"


class RespuestaTipoCuentaBancaria(BaseModel):
    id: int
    nombre: str
    condominio_id: int
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaTiposCuentaBancaria(BaseModel):
    items: List[RespuestaTipoCuentaBancaria]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
