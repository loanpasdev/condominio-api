from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time


class SolicitudCrearAsamblea(BaseModel):
    condominio_id: Optional[int] = None
    tipo: str = "ordinaria"
    titulo: str
    fecha: Optional[date] = None
    hora: Optional[time] = None
    quorum_requerido: Optional[float] = 0
    descripcion: Optional[str] = None
    lugar: Optional[str] = None


class SolicitudActualizarAsamblea(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    fecha: Optional[date] = None
    hora: Optional[time] = None
    lugar: Optional[str] = None
    quorum_requerido: Optional[float] = None
    quorum_obtenido: Optional[float] = None
    estado: Optional[str] = None


class RespuestaAsamblea(BaseModel):
    id: int
    condominio_id: Optional[int] = None
    tipo: str
    titulo: str
    descripcion: Optional[str] = None
    fecha: date
    hora: time
    lugar: Optional[str] = None
    quorum_requerido: float
    quorum_obtenido: float
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaAsambleas(BaseModel):
    items: List[RespuestaAsamblea]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
