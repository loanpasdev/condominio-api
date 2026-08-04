from app.dominio.entidad_base import Entidad
from datetime import date


class Cobro(Entidad):
    def __init__(
        self,
        condominio_id: int,
        categoria_id: int,
        descripcion: str,
        monto: float,
        fecha: date,
        proveedor_id: int = None,
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.categoria_id = categoria_id
        self.descripcion = descripcion
        self.monto = monto
        self.fecha = fecha
        self.proveedor_id = proveedor_id
