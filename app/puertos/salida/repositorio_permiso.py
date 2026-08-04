from abc import ABC, abstractmethod
from typing import List


class RepositorioPermiso(ABC):
    @abstractmethod
    def obtener_modulos_por_rol(self, rol: str) -> List[str]:
        pass

    @abstractmethod
    def obtener_todos_los_modulos(self) -> List[dict]:
        pass

    @abstractmethod
    def asignar_modulos_a_rol(self, rol: str, codigos_modulos: List[str]) -> None:
        pass
