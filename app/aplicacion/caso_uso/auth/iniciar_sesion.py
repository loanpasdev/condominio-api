from app.dominio.usuario.entidad import Usuario
from app.dominio.usuario.valores import RolUsuario, EstadoUsuario
from app.dominio.usuario.excepciones import CredencialesInvalidas, UsuarioYaExiste
from app.puertos.salida.repositorio_usuario import RepositorioUsuario
from app.puertos.salida.repositorio_permiso import RepositorioPermiso
from app.infraestructura.auth.hash_contrasena import hash_contrasena, verificar_contrasena
from app.infraestructura.auth.gestor_tokens import crear_token_acceso


class IniciarSesion:
    """Caso de uso: Iniciar sesion"""

    def __init__(self, repositorio: RepositorioUsuario, repositorio_permiso: RepositorioPermiso = None):
        self.repositorio = repositorio
        self.repositorio_permiso = repositorio_permiso

    def ejecutar(self, correo: str, contrasena: str) -> dict:
        usuario = self.repositorio.obtener_por_correo(correo)
        if not usuario:
            raise CredencialesInvalidas("Credenciales invalidas")

        if not verificar_contrasena(contrasena, usuario.contrasena_hash):
            raise CredencialesInvalidas("Credenciales invalidas")

        if usuario.estado != EstadoUsuario.ACTIVO:
            raise CredencialesInvalidas("Usuario desactivado")

        token = crear_token_acceso(
            datos={"sub": str(usuario.id), "correo": usuario.correo, "rol": usuario.rol.value}
        )

        modulos = []
        if self.repositorio_permiso:
            modulos = self.repositorio_permiso.obtener_modulos_por_rol(usuario.rol.value)

        return {
            "access_token": token,
            "token_type": "bearer",
            "usuario": {
                "id": usuario.id,
                "correo": usuario.correo,
                "nombre": usuario.nombre,
                "apellido": usuario.apellido,
                "telefono": usuario.telefono,
                "rol": usuario.rol.value,
            },
            "modulos": modulos,
        }


class RegistrarUsuario:
    """Caso de uso: Registrar nuevo usuario"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(self, correo: str, contrasena: str, nombre: str, rol: str, apellido: str = None, telefono: str = None, cedula: str = None) -> Usuario:
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


class ObtenerUsuarioActual:
    """Caso de uso: Obtener usuario actual desde token"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(self, usuario_id: int) -> Usuario:
        usuario = self.repositorio.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        return usuario


class CambiarContrasena:
    """Caso de uso: Cambiar contrasena del usuario autenticado"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(self, usuario_id: int, contrasena_actual: str, contrasena_nueva: str):
        usuario = self.repositorio.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        if not verificar_contrasena(contrasena_actual, usuario.contrasena_hash):
            raise CredencialesInvalidas("La contraseña actual es incorrecta")

        nuevo_hash = hash_contrasena(contrasena_nueva)
        self.repositorio.actualizar_contrasena(usuario_id, nuevo_hash)


class ActualizarPerfil:
    """Caso de uso: Actualizar perfil del usuario autenticado"""

    def __init__(self, repositorio: RepositorioUsuario):
        self.repositorio = repositorio

    def ejecutar(self, usuario_id: int, nombre: str = None, apellido: str = None, telefono: str = None, cedula: str = None) -> Usuario:
        usuario = self.repositorio.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado")

        if nombre is not None:
            usuario.nombre = nombre
        if apellido is not None:
            usuario.apellido = apellido
        if telefono is not None:
            usuario.telefono = telefono
        if cedula is not None:
            usuario.cedula = cedula

        return self.repositorio.actualizar(usuario)
