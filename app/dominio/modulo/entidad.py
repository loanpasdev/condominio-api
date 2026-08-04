from app.dominio.entidad_base import Entidad


class Modulo(Entidad):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        descripcion: str = None,
        id: int = None,
    ):
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
