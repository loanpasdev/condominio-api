from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearCondominio(BaseModel):
    nombre: str
    rif: str
    direccion: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    logo: Optional[str] = None


class SolicitudActualizarCondominio(BaseModel):
    nombre: str
    rif: str
    direccion: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    logo: Optional[str] = None


class RespuestaCondominio(BaseModel):
    id: int
    nombre: str
    rif: str
    direccion: str
    telefono: Optional[str] = None
    email: Optional[str] = None
    logo: Optional[str] = None

    class Config:
        from_attributes = True


class RespuestaListaCondominios(BaseModel):
    items: List[RespuestaCondominio]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
