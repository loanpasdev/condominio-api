from app.dominio.entidad_base import Entidad
from app.dominio.usuario.valores import EstadoUsuario


class AreaComun(Entidad):
    def __init__(
        self,
        nombre: str,
        condominio_id: int,
        descripcion: str = None,
        capacidad: int = None,
        tarifa: float = 0,
        hora_inicio: str = None,
        hora_fin: str = None,
        estado: EstadoUsuario = EstadoUsuario.ACTIVO,
        id: int = None,
    ):
        super().__init__(id)
        self.nombre = nombre
        self.condominio_id = condominio_id
        self.descripcion = descripcion
        self.capacidad = capacidad
        self.tarifa = tarifa
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado
