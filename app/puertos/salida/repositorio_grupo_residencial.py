from abc import ABC, abstractmethod
from typing import Optional, List
from app.dominio.grupo_residencial import GrupoResidencial


class RepositorioGrupoResidencial(ABC):
    """Puerto de salida para repositorio de grupos residenciales"""

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[GrupoResidencial]:
        pass

    @abstractmethod
    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[GrupoResidencial], int]:
        pass

    @abstractmethod
    def crear(self, grupo: GrupoResidencial) -> GrupoResidencial:
        pass

    @abstractmethod
    def actualizar(self, grupo: GrupoResidencial) -> GrupoResidencial:
        pass

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        pass

    @abstractmethod
    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        pass
