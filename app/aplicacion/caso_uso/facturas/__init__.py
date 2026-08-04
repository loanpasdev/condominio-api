from app.dominio.factura.entidad import Factura
from app.dominio.factura.excepciones import FacturaNoExiste
from app.puertos.salida.repositorio_factura import RepositorioFactura


class CrearFactura:
    def __init__(self, repositorio: RepositorioFactura):
        self.repositorio = repositorio

    def ejecutar(self, condominio_id: int, numero: str, descripcion: str, monto_total: float, fecha, distribucion: str, destino_id: int = None) -> Factura:
        return self.repositorio.crear(Factura(
            condominio_id=condominio_id, numero=numero,
            descripcion=descripcion, monto_total=monto_total,
            fecha=fecha, distribucion=distribucion, destino_id=destino_id,
        ))


class ListarFacturas:
    def __init__(self, repositorio: RepositorioFactura):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)


class ObtenerFactura:
    def __init__(self, repositorio: RepositorioFactura):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Factura:
        factura = self.repositorio.obtener_por_id(id)
        if not factura:
            raise FacturaNoExiste("Factura no encontrada")
        return factura


class ActualizarFactura:
    def __init__(self, repositorio: RepositorioFactura):
        self.repositorio = repositorio

    def ejecutar(self, id: int, numero: str, descripcion: str, monto_total: float, fecha, distribucion: str, destino_id: int, estado: str) -> Factura:
        factura = self.repositorio.obtener_por_id(id)
        if not factura:
            raise FacturaNoExiste("Factura no encontrada")
        factura.numero = numero
        factura.descripcion = descripcion
        factura.monto_total = monto_total
        factura.fecha = fecha
        factura.distribucion = distribucion
        factura.destino_id = destino_id
        factura.estado = estado
        return self.repositorio.actualizar(factura)


class EliminarFactura:
    def __init__(self, repositorio: RepositorioFactura):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        factura = self.repositorio.obtener_por_id(id)
        if not factura:
            raise FacturaNoExiste("Factura no encontrada")
        return self.repositorio.eliminar(id)
