from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.tipo_cuenta_bancaria.entidad import TipoCuentaBancaria


class RepositorioTipoCuentaBancaria(ABC):
    """Puerto de salida para repositorio de tipos de cuenta bancaria"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[TipoCuentaBancaria]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[TipoCuentaBancaria], int]:
        pass

    @abstractmethod
    def crear(self, tipo_cuenta: TipoCuentaBancaria) -> TipoCuentaBancaria:
        pass

    @abstractmethod
    def actualizar(self, tipo_cuenta: TipoCuentaBancaria) -> TipoCuentaBancaria:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        pass
