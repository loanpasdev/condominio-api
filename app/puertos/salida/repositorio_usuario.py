from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.usuario.entidad import Usuario


class RepositorioUsuario(ABC):
    """Puerto de salida para repositorio de usuarios"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        pass

    @abstractmethod
    def obtener_por_correo(self, correo: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def obtener_todos(self) -> List[Usuario]:
        pass

    @abstractmethod
    def crear(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def actualizar(self, usuario: Usuario) -> Usuario:
        pass

    @abstractmethod
    def actualizar_contrasena(self, usuario_id: int, hash_contrasena: str) -> None:
        pass

    @abstractmethod
    def eliminar(self, usuario_id: int) -> None:
        pass
