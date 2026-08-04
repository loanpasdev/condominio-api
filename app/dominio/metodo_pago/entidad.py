from app.dominio.entidad_base import Entidad
from app.dominio.usuario.valores import EstadoUsuario


class MetodoPago(Entidad):
    def __init__(
        self,
        nombre: str,
        condominio_id: int,
        estado: EstadoUsuario = EstadoUsuario.ACTIVO,
        id: int = None,
    ):
        super().__init__(id)
        self.nombre = nombre
        self.condominio_id = condominio_id
        self.estado = estado
