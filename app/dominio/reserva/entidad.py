from app.dominio.entidad_base import Entidad


class Reserva(Entidad):
    def __init__(
        self,
        condominio_id: int,
        area_comun_id: int,
        propietario_id: int,
        fecha,
        hora_inicio,
        hora_fin,
        estado: str = "confirmada",
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.area_comun_id = area_comun_id
        self.propietario_id = propietario_id
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
