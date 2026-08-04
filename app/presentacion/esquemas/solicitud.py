from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearSolicitud(BaseModel):
    condominio_id: Optional[int] = None
    propietario_id: Optional[int] = None
    titulo: str
    descripcion: str
    categoria: str = "otro"
    prioridad: str = "media"
    responsable: Optional[str] = None


class SolicitudActualizarSolicitud(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    categoria: Optional[str] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None
    responsable: Optional[str] = None


class RespuestaSolicitud(BaseModel):
    id: int
    condominio_id: Optional[int] = None
    propietario_id: Optional[int] = None
    titulo: str
    descripcion: str
    categoria: str
    prioridad: str
    estado: str
    responsable: Optional[str] = None

    class Config:
        from_attributes = True


class RespuestaListaSolicitudes(BaseModel):
    items: List[RespuestaSolicitud]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
