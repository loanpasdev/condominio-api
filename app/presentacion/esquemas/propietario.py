from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearPropietario(BaseModel):
    condominio_id: int
    nombre: str
    apellido: str
    cedula: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    usuario_id: Optional[int] = None


class SolicitudActualizarPropietario(BaseModel):
    condominio_id: Optional[int] = None
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    cedula: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[bool] = None
    usuario_id: Optional[int] = None


class RespuestaPropietario(BaseModel):
    id: int
    condominio_id: int
    usuario_id: Optional[int] = None
    nombre: str
    apellido: str
    cedula: str
    correo: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    estado: bool

    class Config:
        from_attributes = True


class RespuestaListaPropietarios(BaseModel):
    propietarios: List[RespuestaPropietario]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
