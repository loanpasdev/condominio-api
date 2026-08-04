from pydantic import BaseModel, Field
from typing import Optional


class ModuloCrear(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None


class ModuloActualizar(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50)
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None


class ModuloRespuesta(BaseModel):
    id: int
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    fecha_creacion: Optional[str] = None
    fecha_actualizacion: Optional[str] = None

    class Config:
        from_attributes = True
