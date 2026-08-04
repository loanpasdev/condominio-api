from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.recibo.entidad import Recibo


class RepositorioRecibo(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Recibo]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, factura_id: int = None, unidad_id: int = None, propietario_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Recibo], int]:
        pass

    @abstractmethod
    def crear(self, recibo: Recibo) -> Recibo:
        pass

    @abstractmethod
    def actualizar(self, recibo: Recibo) -> Recibo:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
