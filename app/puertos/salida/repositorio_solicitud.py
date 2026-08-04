from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.solicitud.entidad import Solicitud


class RepositorioSolicitud(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Solicitud]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, propietario_id: int = None, estado: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Solicitud], int]:
        pass

    @abstractmethod
    def crear(self, solicitud: Solicitud) -> Solicitud:
        pass

    @abstractmethod
    def actualizar(self, solicitud: Solicitud) -> Solicitud:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
