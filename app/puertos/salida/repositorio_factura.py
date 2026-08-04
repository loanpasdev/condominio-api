from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.factura.entidad import Factura


class RepositorioFactura(ABC):
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Factura]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Factura], int]:
        pass

    @abstractmethod
    def crear(self, factura: Factura) -> Factura:
        pass

    @abstractmethod
    def actualizar(self, factura: Factura) -> Factura:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass
