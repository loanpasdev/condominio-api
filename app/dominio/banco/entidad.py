from app.dominio.entidad_base import Entidad


class Banco(Entidad):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        id: int = None,
    ):
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre
