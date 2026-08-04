from app.dominio.entidad_base import Entidad


class Asamblea(Entidad):
    def __init__(
        self,
        condominio_id: int,
        tipo: str,
        titulo: str,
        fecha,
        hora,
        quorum_requerido: float,
        descripcion: str = None,
        lugar: str = None,
        quorum_obtenido: float = 0,
        estado: str = "programada",
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.tipo = tipo
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.hora = hora
        self.lugar = lugar
        self.quorum_requerido = quorum_requerido
        self.quorum_obtenido = quorum_obtenido
        self.estado = estado
