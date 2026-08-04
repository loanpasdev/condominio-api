from app.dominio.entidad_base import Entidad


class Notificacion(Entidad):
    def __init__(
        self,
        condominio_id: int,
        titulo: str,
        mensaje: str,
        tipo: str,
        usuario_id: int = None,
        leida: bool = False,
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.usuario_id = usuario_id
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo
        self.leida = leida
