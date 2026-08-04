from app.dominio.entidad_base import Entidad


class Solicitud(Entidad):
    def __init__(
        self,
        condominio_id: int,
        propietario_id: int,
        titulo: str,
        descripcion: str,
        categoria: str,
        prioridad: str = "media",
        estado: str = "abierta",
        responsable: str = None,
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.propietario_id = propietario_id
        self.titulo = titulo
        self.descripcion = descripcion
        self.categoria = categoria
        self.prioridad = prioridad
        self.estado = estado
        self.responsable = responsable
