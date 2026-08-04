from abc import ABC
from datetime import datetime
from typing import Optional


class Entidad(ABC):
    """Clase base para todas las entidades del dominio"""

    def __init__(self, id: Optional[int] = None):
        self.id = id
        self.fecha_creacion: datetime = datetime.utcnow()
        self.fecha_actualizacion: datetime = datetime.utcnow()

    def __eq__(self, other):
        if not isinstance(other, Entidad):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
