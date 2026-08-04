from app.dominio.entidad_base import Entidad


class Propietario(Entidad):
    def __init__(
        self,
        condominio_id: int,
        nombre: str,
        apellido: str,
        cedula: str,
        correo: str,
        telefono: str = None,
        direccion: str = None,
        estado: bool = True,
        usuario_id: int = None,
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.correo = correo
        self.telefono = telefono
        self.direccion = direccion
        self.estado = estado
        self.usuario_id = usuario_id
