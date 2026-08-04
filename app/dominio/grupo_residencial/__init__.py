from app.dominio.entidad_base import Entidad


class GrupoResidencial(Entidad):
    def __init__(
        self,
        condominio_id: int,
        nombre: str,
        descripcion: str = None,
        estado: bool = True,
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
