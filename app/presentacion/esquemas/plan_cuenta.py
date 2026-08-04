from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearPlanCuenta(BaseModel):
    codigo: str
    nombre: str
    tipo: str
    descripcion: Optional[str] = None
    padre_id: Optional[int] = None


class SolicitudActualizarPlanCuenta(BaseModel):
    codigo: str
    nombre: str
    tipo: str
    descripcion: Optional[str] = None
    padre_id: Optional[int] = None
    activo: bool = True


class RespuestaPlanCuenta(BaseModel):
    id: int
    codigo: str
    nombre: str
    tipo: str
    descripcion: Optional[str] = None
    padre_id: Optional[int] = None
    activo: bool

    class Config:
        from_attributes = True


class RespuestaListaPlanCuentas(BaseModel):
    items: List[RespuestaPlanCuenta]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
