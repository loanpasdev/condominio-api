from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearAreaComun(BaseModel):
    nombre: str
    condominio_id: int
    descripcion: Optional[str] = None
    capacidad: Optional[int] = None
    tarifa: float = 0
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None


class SolicitudActualizarAreaComun(BaseModel):
    nombre: str
    condominio_id: int
    descripcion: Optional[str] = None
    capacidad: Optional[int] = None
    tarifa: float = 0
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    estado: str = "activo"


class RespuestaAreaComun(BaseModel):
    id: int
    nombre: str
    condominio_id: int
    descripcion: Optional[str] = None
    capacidad: Optional[int] = None
    tarifa: float
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaAreasComunes(BaseModel):
    items: List[RespuestaAreaComun]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
