from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearNotificacion(BaseModel):
    condominio_id: int
    titulo: str
    mensaje: str
    tipo: str
    usuario_id: Optional[int] = None


class SolicitudActualizarNotificacion(BaseModel):
    titulo: str
    mensaje: str
    tipo: str
    leida: bool = False


class RespuestaNotificacion(BaseModel):
    id: int
    condominio_id: int
    usuario_id: Optional[int] = None
    titulo: str
    mensaje: str
    tipo: str
    leida: bool

    class Config:
        from_attributes = True


class RespuestaListaNotificaciones(BaseModel):
    items: List[RespuestaNotificacion]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
