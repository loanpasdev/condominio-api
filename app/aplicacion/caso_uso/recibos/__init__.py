from app.dominio.recibo.entidad import Recibo
from app.dominio.recibo.excepciones import ReciboNoExiste
from app.puertos.salida.repositorio_recibo import RepositorioRecibo


class CrearRecibo:
    def __init__(self, repositorio: RepositorioRecibo):
        self.repositorio = repositorio

    def ejecutar(self, condominio_id: int = None, factura_id: int = None, unidad_id: int = None, propietario_id: int = None, subtotal: float = 0, total: float = 0, mora: float = 0) -> Recibo:
        return self.repositorio.crear(Recibo(
            condominio_id=condominio_id or 1, factura_id=factura_id,
            unidad_id=unidad_id, propietario_id=propietario_id,
            subtotal=subtotal, total=total, mora=mora,
        ))


class ListarRecibos:
    def __init__(self, repositorio: RepositorioRecibo):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, factura_id: int = None, unidad_id: int = None, propietario_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, factura_id=factura_id, unidad_id=unidad_id, propietario_id=propietario_id, pagina=pagina, por_pagina=por_pagina)


class ObtenerRecibo:
    def __init__(self, repositorio: RepositorioRecibo):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Recibo:
        recibo = self.repositorio.obtener_por_id(id)
        if not recibo:
            raise ReciboNoExiste("Recibo no encontrado")
        return recibo


class ActualizarRecibo:
    def __init__(self, repositorio: RepositorioRecibo):
        self.repositorio = repositorio

    def ejecutar(self, id: int, subtotal: float = None, mora: float = None, total: float = None, estado: str = None) -> Recibo:
        recibo = self.repositorio.obtener_por_id(id)
        if not recibo:
            raise ReciboNoExiste("Recibo no encontrado")
        if subtotal is not None: recibo.subtotal = subtotal
        if mora is not None: recibo.mora = mora
        if total is not None: recibo.total = total
        if estado is not None: recibo.estado = estado
        return self.repositorio.actualizar(recibo)


class EliminarRecibo:
    def __init__(self, repositorio: RepositorioRecibo):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        recibo = self.repositorio.obtener_por_id(id)
        if not recibo:
            raise ReciboNoExiste("Recibo no encontrado")
        return self.repositorio.eliminar(id)
