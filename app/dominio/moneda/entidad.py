from app.dominio.entidad_base import Entidad
from app.dominio.usuario.valores import EstadoUsuario


class Moneda(Entidad):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        simbolo: str,
        estado: EstadoUsuario = EstadoUsuario.ACTIVO,
        es_base: bool = False,
        tasa_cambio: float = 1.0,
        id: int = None,
    ):
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre
        self.simbolo = simbolo
        self.estado = estado
        self.es_base = es_base
        self.tasa_cambio = tasa_cambio
