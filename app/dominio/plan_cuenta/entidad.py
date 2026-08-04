from app.dominio.entidad_base import Entidad


class PlanCuenta(Entidad):
    def __init__(
        self,
        codigo: str,
        nombre: str,
        tipo: str,
        descripcion: str = None,
        padre_id: int = None,
        activo: bool = True,
        id: int = None,
    ):
        super().__init__(id)
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.descripcion = descripcion
        self.padre_id = padre_id
        self.activo = activo
