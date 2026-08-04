from pydantic import BaseModel
from typing import Optional, List


class SolicitudCrearCuentaBancaria(BaseModel):
    condominio_id: Optional[int] = None
    banco_id: Optional[int] = None
    tipo_cuenta_id: Optional[int] = None
    numero_cuenta: str = ""
    titular: str = ""
    moneda_id: Optional[int] = None
    saldo: float = 0


class SolicitudActualizarCuentaBancaria(BaseModel):
    banco_id: Optional[int] = None
    tipo_cuenta_id: Optional[int] = None
    numero_cuenta: Optional[str] = None
    titular: Optional[str] = None
    moneda_id: Optional[int] = None
    saldo: Optional[float] = None
    estado: Optional[str] = None


class RespuestaCuentaBancaria(BaseModel):
    id: int
    condominio_id: Optional[int] = None
    banco_id: Optional[int] = None
    tipo_cuenta_id: Optional[int] = None
    numero_cuenta: str
    titular: str
    moneda_id: Optional[int] = None
    saldo: float
    estado: str

    class Config:
        from_attributes = True


class RespuestaListaCuentasBancarias(BaseModel):
    items: List[RespuestaCuentaBancaria]
    total: int
    pagina: int
    por_pagina: int
    paginas: int
