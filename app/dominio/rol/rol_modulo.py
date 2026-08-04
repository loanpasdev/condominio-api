from app.dominio.entidad_base import Entidad


class RolModulo(Entidad):
    def __init__(
        self,
        rol: str,
        modulo_id: int,
        id: int = None,
    ):
        super().__init__(id)
        self.rol = rol
        self.modulo_id = modulo_id
