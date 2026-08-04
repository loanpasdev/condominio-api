from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.metodo_pago.entidad import MetodoPago


class RepositorioMetodoPago(ABC):
    """Puerto de salida para repositorio de metodos de pago"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[MetodoPago]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[MetodoPago], int]:
        pass

    @abstractmethod
    def crear(self, metodo_pago: MetodoPago) -> MetodoPago:
        pass

    @abstractmethod
    def actualizar(self, metodo_pago: MetodoPago) -> MetodoPago:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        pass
