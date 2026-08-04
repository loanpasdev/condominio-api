from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.notificacion.entidad import Notificacion


class RepositorioNotificacion(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Notificacion]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, usuario_id: int = None, tipo: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Notificacion], int]:
        pass

    @abstractmethod
    def crear(self, notificacion: Notificacion) -> Notificacion:
        pass

    @abstractmethod
    def actualizar(self, notificacion: Notificacion) -> Notificacion:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
