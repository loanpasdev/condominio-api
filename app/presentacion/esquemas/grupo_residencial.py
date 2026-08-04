from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearGrupoResidencial(BaseModel):
    condominio_id: int
    nombre: str
    descripcion: Optional[str] = None


class SolicitudActualizarGrupoResidencial(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    estado: bool = True


class RespuestaGrupoResidencial(BaseModel):
    id: int
    condominio_id: int
    nombre: str
    descripcion: Optional[str] = None
    estado: bool

    class Config:
        from_attributes = True


class RespuestaListaGruposResidenciales(BaseModel):
    items: List[RespuestaGrupoResidencial]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
