from app.dominio.cobro.entidad import Cobro
from app.dominio.cobro.excepciones import CobroNoExiste
from app.puertos.salida.repositorio_cobro import RepositorioCobro
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearCobro:
    def __init__(self, repositorio: RepositorioCobro, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, condominio_id: int = None, categoria_id: int = None, descripcion: str = '', monto: float = 0, fecha=None, proveedor_id: int = None) -> Cobro:
        return self.repositorio.crear(Cobro(
            condominio_id=condominio_id or 1, categoria_id=categoria_id,
            descripcion=descripcion, monto=monto, fecha=fecha,
            proveedor_id=proveedor_id,
        ))


class ListarCobros:
    def __init__(self, repositorio: RepositorioCobro):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)


class ObtenerCobro:
    def __init__(self, repositorio: RepositorioCobro):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Cobro:
        cobro = self.repositorio.obtener_por_id(id)
        if not cobro:
            raise CobroNoExiste("Cobro no encontrado")
        return cobro


class ActualizarCobro:
    def __init__(self, repositorio: RepositorioCobro):
        self.repositorio = repositorio

    def ejecutar(self, id: int, categoria_id: int = None, descripcion: str = None, monto: float = None, fecha=None, proveedor_id: int = None) -> Cobro:
        cobro = self.repositorio.obtener_por_id(id)
        if not cobro:
            raise CobroNoExiste("Cobro no encontrado")
        if categoria_id is not None: cobro.categoria_id = categoria_id
        if descripcion is not None: cobro.descripcion = descripcion
        if monto is not None: cobro.monto = monto
        if fecha is not None: cobro.fecha = fecha
        if proveedor_id is not None: cobro.proveedor_id = proveedor_id
        return self.repositorio.actualizar(cobro)


class EliminarCobro:
    def __init__(self, repositorio: RepositorioCobro):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        cobro = self.repositorio.obtener_por_id(id)
        if not cobro:
            raise CobroNoExiste("Cobro no encontrado")
        return self.repositorio.eliminar(id)
