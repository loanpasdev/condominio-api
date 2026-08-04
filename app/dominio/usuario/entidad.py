from app.dominio.entidad_base import Entidad
from app.dominio.usuario.valores import RolUsuario, EstadoUsuario


class Usuario(Entidad):
    def __init__(
        self,
        correo: str,
        contrasena_hash: str,
        nombre: str,
        rol: RolUsuario,
        apellido: str = None,
        telefono: str = None,
        cedula: str = None,
        propietario_id: int = None,
        estado: EstadoUsuario = EstadoUsuario.ACTIVO,
        ultimo_acceso=None,
        id: int = None,
    ):
        super().__init__(id)
        self.correo = correo
        self.contrasena_hash = contrasena_hash
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.cedula = cedula
        self.rol = rol
        self.propietario_id = propietario_id
        self.estado = estado
        self.ultimo_acceso = ultimo_acceso
