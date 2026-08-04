from app.dominio.entidad_base import Entidad


class Cuota(Entidad):
    def __init__(
        self,
        condominio_id: int,
        unidad_id: int,
        mes: int,
        anio: int,
        monto_total: float,
        estado: str = "pendiente",
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.unidad_id = unidad_id
        self.mes = mes
        self.anio = anio
        self.monto_total = monto_total
        self.estado = estado
