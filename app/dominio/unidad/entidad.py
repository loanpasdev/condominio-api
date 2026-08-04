from app.dominio.entidad_base import Entidad


class Unidad(Entidad):
    def __init__(
        self,
        condominio_id: int,
        tipo_unidad_id: int,
        numero: str,
        metraje: float,
        porcentual: float,
        propietario_id: int = None,
        piso: str = None,
        grupo_residencial_id: int = None,
        habitaciones: int = 0,
        banios: int = 0,
        terraza: bool = False,
        balcon: bool = False,
        parking: bool = False,
        notas: str = None,
        estado: bool = True,
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.tipo_unidad_id = tipo_unidad_id
        self.numero = numero
        self.metraje = metraje
        self.porcentual = porcentual
        self.propietario_id = propietario_id
        self.piso = piso
        self.grupo_residencial_id = grupo_residencial_id
        self.habitaciones = habitaciones
        self.banios = banios
        self.terraza = terraza
        self.balcon = balcon
        self.parking = parking
        self.notas = notas
        self.estado = estado
