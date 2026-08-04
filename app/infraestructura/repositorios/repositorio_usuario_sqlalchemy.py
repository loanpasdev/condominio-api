from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.usuario.entidad import Usuario
from app.dominio.usuario.valores import RolUsuario, EstadoUsuario
from app.puertos.salida.repositorio_usuario import RepositorioUsuario
from app.infraestructura.modelado.modelo_usuario import UsuarioModelo


class RepositorioUsuarioSQLAlchemy(RepositorioUsuario):
    """Implementacion del repositorio de usuarios con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        modelo = self.db.query(UsuarioModelo).filter(
            UsuarioModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        modelo = self.db.query(UsuarioModelo).filter(
            UsuarioModelo.correo == correo
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def obtener_todos(self) -> List[Usuario]:
        modelos = self.db.query(UsuarioModelo).all()
        return [self._mapear_a_entidad(m) for m in modelos]

    def crear(self, usuario: Usuario) -> Usuario:
        modelo = UsuarioModelo(
            correo=usuario.correo,
            contrasena_hash=usuario.contrasena_hash,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            telefono=usuario.telefono,
            cedula=usuario.cedula,
            rol=usuario.rol.value,
            propietario_id=usuario.propietario_id,
            estado=usuario.estado.value,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, usuario: Usuario) -> Usuario:
        modelo = self.db.query(UsuarioModelo).filter(
            UsuarioModelo.id == usuario.id
        ).first()
        if not modelo:
            return None
        modelo.correo = usuario.correo
        modelo.nombre = usuario.nombre
        modelo.apellido = usuario.apellido
        modelo.telefono = usuario.telefono
        modelo.cedula = usuario.cedula
        modelo.rol = usuario.rol.value
        modelo.estado = usuario.estado.value
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar_contrasena(self, usuario_id: int, hash_contrasena: str) -> None:
        modelo = self.db.query(UsuarioModelo).filter(
            UsuarioModelo.id == usuario_id
        ).first()
        if modelo:
            modelo.contrasena_hash = hash_contrasena
            self.db.commit()

    def eliminar(self, usuario_id: int) -> None:
        self.db.query(UsuarioModelo).filter(
            UsuarioModelo.id == usuario_id
        ).delete()
        self.db.commit()

    def _mapear_a_entidad(self, modelo: UsuarioModelo) -> Usuario:
        return Usuario(
            id=modelo.id,
            correo=modelo.correo,
            contrasena_hash=modelo.contrasena_hash,
            nombre=modelo.nombre,
            apellido=modelo.apellido,
            telefono=modelo.telefono,
            cedula=modelo.cedula,
            rol=RolUsuario(modelo.rol),
            propietario_id=modelo.propietario_id,
            estado=EstadoUsuario(modelo.estado),
            ultimo_acceso=modelo.ultimo_acceso,
        )
