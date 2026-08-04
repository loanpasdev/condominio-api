from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearProveedor(BaseModel):
    nombre: str
    rif: str
    condominio_id: int
    telefono: Optional[str] = None
    email: Optional[str] = None


class SolicitudActualizarProveedor(BaseModel):
    nombre: str
    rif: str
    condominio_id: int
    telefono: Optional[str] = None
    email: Optional[str] = None
    estado: str = "activo"


class RespuestaProveedor(BaseModel):
    id: int
    nombre: str
    rif: str
    condominio_id: int
    telefono: Optional[str] = None
    email: Optional[str] = None
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaProveedores(BaseModel):
    items: List[RespuestaProveedor]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
