from app.dominio.entidad_base import Entidad


class Recibo(Entidad):
    def __init__(
        self,
        condominio_id: int,
        factura_id: int,
        unidad_id: int,
        propietario_id: int,
        subtotal: float,
        total: float,
        mora: float = 0,
        estado: str = "pendiente",
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.factura_id = factura_id
        self.unidad_id = unidad_id
        self.propietario_id = propietario_id
        self.subtotal = subtotal
        self.mora = mora
        self.total = total
        self.estado = estado
