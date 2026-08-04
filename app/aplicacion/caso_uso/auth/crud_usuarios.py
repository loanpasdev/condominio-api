from typing import List
from app.dominio.usuario.entidad import Usuario
from app.dominio.usuario.valores import RolUsuario, EstadoUsuario
from app.dominio.usuario.excepciones import UsuarioYaExiste, UsuarioNoEncontrado
from app.puertos.salida.repositorio_usuario import RepositorioUsuario
from app.infraestructura.auth.hash_contrasena import hash_contrasena


class ListarUsuarios:
    """Caso de uso: Listar todos los usuarios"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(self) -> List[Usuario]:
        return self.repositorio.obtener_todos()


class ObtenerUsuario:
    """Caso de uso: Obtener un usuario por ID"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(self, usuario_id: int) -> Usuario:
        usuario = self.repositorio.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado("Usuario no encontrado")
        return usuario


class CrearUsuario:
    """Caso de uso: Crear un nuevo usuario"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(
        self,
        correo: str,
        contrasena: str,
        nombre: str,
        rol: str,
        apellido: str = None,
        telefono: str = None,
        cedula: str = None,
    ) -> Usuario:
        existente = self.repositorio.obtener_por_correo(correo)
        if existente:
            raise UsuarioYaExiste(f"Ya existe un usuario con correo {correo}")

        usuario = Usuario(
            correo=correo,
            contrasena_hash=hash_contrasena(contrasena),
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            cedula=cedula,
            rol=RolUsuario(rol),
            estado=EstadoUsuario.ACTIVO,
        )
        return self.repositorio.crear(usuario)


class ActualizarUsuario:
    """Caso de uso: Actualizar un usuario existente"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(
        self,
        usuario_id: int,
        nombre: str = None,
        apellido: str = None,
        telefono: str = None,
        cedula: str = None,
        correo: str = None,
        rol: str = None,
        estado: str = None,
    ) -> Usuario:
        usuario = self.repositorio.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado("Usuario no encontrado")

        if nombre is not None:
            usuario.nombre = nombre
        if apellido is not None:
            usuario.apellido = apellido
        if telefono is not None:
            usuario.telefono = telefono
        if cedula is not None:
            usuario.cedula = cedula
        if correo is not None:
            existente = self.repositorio.obtener_por_correo(correo)
            if existente and existente.id != usuario_id:
                raise UsuarioYaExiste(f"Ya existe un usuario con correo {correo}")
            usuario.correo = correo
        if rol is not None:
            usuario.rol = RolUsuario(rol)
        if estado is not None:
            usuario.estado = EstadoUsuario(estado)

        return self.repositorio.actualizar(usuario)


class EliminarUsuario:
    """Caso de uso: Eliminar un usuario"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(self, usuario_id: int):
        usuario = self.repositorio.obtener_por_id(usuario_id)
        if not usuario:
            raise UsuarioNoEncontrado("Usuario no encontrado")
        self.repositorio.eliminar(usuario_id)
