from pydantic import BaseModel
from typing import Optional, List
from datetime import date, time


class SolicitudCrearReserva(BaseModel):
    condominio_id: Optional[int] = None
    area_comun_id: Optional[int] = None
    propietario_id: Optional[int] = None
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None


class SolicitudActualizarReserva(BaseModel):
    fecha: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    estado: Optional[str] = None


class RespuestaReserva(BaseModel):
    id: int
    condominio_id: Optional[int] = None
    area_comun_id: Optional[int] = None
    propietario_id: Optional[int] = None
    fecha: date
    hora_inicio: time
    hora_fin: time
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaReservas(BaseModel):
    items: List[RespuestaReserva]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
