from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.proveedor.entidad import Proveedor


class RepositorioProveedor(ABC):
    """Puerto de salida para repositorio de proveedores"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Proveedor]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Proveedor], int]:
        pass

    @abstractmethod
    def crear(self, proveedor: Proveedor) -> Proveedor:
        pass

    @abstractmethod
    def actualizar(self, proveedor: Proveedor) -> Proveedor:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        pass
