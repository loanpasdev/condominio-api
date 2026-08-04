from app.dominio.entidad_base import Entidad
from app.dominio.usuario.valores import EstadoUsuario


class Proveedor(Entidad):
    def __init__(
        self,
        nombre: str,
        rif: str,
        condominio_id: int,
        telefono: str = None,
        email: str = None,
        estado: EstadoUsuario = EstadoUsuario.ACTIVO,
        id: int = None,
    ):
        super().__init__(id)
        self.nombre = nombre
        self.rif = rif
        self.condominio_id = condominio_id
        self.telefono = telefono
        self.email = email
        self.estado = estado
