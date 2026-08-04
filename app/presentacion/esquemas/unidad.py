from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearUnidad(BaseModel):
    condominio_id: int
    tipo_unidad_id: int
    numero: str
    metraje: float
    porcentual: float
    propietario_id: Optional[int] = None
    piso: Optional[str] = None
    grupo_residencial_id: Optional[int] = None
    habitaciones: Optional[int] = 0
    banios: Optional[int] = 0
    terraza: Optional[bool] = False
    balcon: Optional[bool] = False
    parking: Optional[bool] = False
    notas: Optional[str] = None


class SolicitudActualizarUnidad(BaseModel):
    condominio_id: int
    tipo_unidad_id: int
    numero: str
    metraje: float
    porcentual: float
    propietario_id: Optional[int] = None
    piso: Optional[str] = None
    grupo_residencial_id: Optional[int] = None
    habitaciones: Optional[int] = 0
    banios: Optional[int] = 0
    terraza: Optional[bool] = False
    balcon: Optional[bool] = False
    parking: Optional[bool] = False
    notas: Optional[str] = None
    estado: bool = True


class RespuestaUnidad(BaseModel):
    id: int
    condominio_id: int
    tipo_unidad_id: int
    propietario_id: Optional[int] = None
    numero: str
    piso: Optional[str] = None
    grupo_residencial_id: Optional[int] = None
    habitaciones: Optional[int] = 0
    banios: Optional[int] = 0
    terraza: Optional[bool] = False
    balcon: Optional[bool] = False
    parking: Optional[bool] = False
    notas: Optional[str] = None
    metraje: float
    porcentual: float
    estado: bool

    class Config:
        from_attributes = True


class SolicitudDuplicarUnidad(BaseModel):
    numero: str


class RespuestaListaUnidades(BaseModel):
    items: List[RespuestaUnidad]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
