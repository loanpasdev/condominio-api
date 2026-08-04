from app.dominio.entidad_base import Entidad
from datetime import datetime


class Pago(Entidad):
    def __init__(
        self,
        condominio_id: int,
        cuota_id: int,
        propietario_id: int,
        monto: float,
        metodo_pago_id: int,
        moneda_id: int,
        fecha_pago: datetime,
        referencia: str = None,
        notas: str = None,
        estado: str = "completado",
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.cuota_id = cuota_id
        self.propietario_id = propietario_id
        self.monto = monto
        self.metodo_pago_id = metodo_pago_id
        self.moneda_id = moneda_id
        self.fecha_pago = fecha_pago
        self.referencia = referencia
        self.notas = notas
        self.estado = estado
