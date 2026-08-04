from app.dominio.pago.entidad import Pago
from app.dominio.pago.excepciones import PagoNoExiste
from app.puertos.salida.repositorio_pago import RepositorioPago
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearPago:
    def __init__(self, repositorio: RepositorioPago, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, condominio_id: int = None, cuota_id: int = None, propietario_id: int = None, monto: float = 0, metodo_pago_id: int = None, moneda_id: int = None, fecha_pago=None, referencia: str = None, notas: str = None) -> Pago:
        return self.repositorio.crear(Pago(
            condominio_id=condominio_id or 1, cuota_id=cuota_id,
            propietario_id=propietario_id, monto=monto,
            metodo_pago_id=metodo_pago_id, moneda_id=moneda_id,
            fecha_pago=fecha_pago, referencia=referencia, notas=notas,
        ))


class ListarPagos:
    def __init__(self, repositorio: RepositorioPago):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, cuota_id: int = None, propietario_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, cuota_id=cuota_id, propietario_id=propietario_id, pagina=pagina, por_pagina=por_pagina)


class ObtenerPago:
    def __init__(self, repositorio: RepositorioPago):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Pago:
        pago = self.repositorio.obtener_por_id(id)
        if not pago:
            raise PagoNoExiste("Pago no encontrado")
        return pago


class ActualizarPago:
    def __init__(self, repositorio: RepositorioPago):
        self.repositorio = repositorio

    def ejecutar(self, id: int, monto: float = None, metodo_pago_id: int = None, moneda_id: int = None, referencia: str = None, fecha_pago=None, notas: str = None, estado: str = None) -> Pago:
        pago = self.repositorio.obtener_por_id(id)
        if not pago:
            raise PagoNoExiste("Pago no encontrado")
        if monto is not None: pago.monto = monto
        if metodo_pago_id is not None: pago.metodo_pago_id = metodo_pago_id
        if moneda_id is not None: pago.moneda_id = moneda_id
        if referencia is not None: pago.referencia = referencia
        if fecha_pago is not None: pago.fecha_pago = fecha_pago
        if notas is not None: pago.notas = notas
        if estado is not None: pago.estado = estado
        return self.repositorio.actualizar(pago)


class EliminarPago:
    def __init__(self, repositorio: RepositorioPago):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        pago = self.repositorio.obtener_por_id(id)
        if not pago:
            raise PagoNoExiste("Pago no encontrado")
        return self.repositorio.eliminar(id)
