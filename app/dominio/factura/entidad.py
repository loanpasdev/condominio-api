from app.dominio.entidad_base import Entidad


class Factura(Entidad):
    def __init__(
        self,
        condominio_id: int,
        numero: str,
        descripcion: str,
        monto_total: float,
        fecha,
        distribucion: str,
        destino_id: int = None,
        estado: str = "pendiente",
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.numero = numero
        self.descripcion = descripcion
        self.monto_total = monto_total
        self.fecha = fecha
        self.distribucion = distribucion
        self.destino_id = destino_id
        self.estado = estado
