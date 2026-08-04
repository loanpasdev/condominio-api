from app.dominio.entidad_base import Entidad


class Condominio(Entidad):
    def __init__(
        self,
        nombre: str,
        rif: str,
        direccion: str,
        telefono: str = None,
        email: str = None,
        logo: str = None,
        id: int = None,
    ):
        super().__init__(id)
        self.nombre = nombre
        self.rif = rif
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.logo = logo
