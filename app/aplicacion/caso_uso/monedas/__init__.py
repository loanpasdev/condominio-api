from app.dominio.moneda.entidad import Moneda
from app.dominio.moneda.excepciones import MonedaNoExiste, MonedaYaExiste
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_moneda import RepositorioMoneda


class CrearMoneda:
    def __init__(self, repositorio: RepositorioMoneda):
        self.repositorio = repositorio

    def ejecutar(self, codigo: str, nombre: str, simbolo: str, es_base: bool = False, tasa_cambio: float = 1.0) -> Moneda:
        if self.repositorio.existe_nombre(nombre):
            raise MonedaYaExiste(f"Ya existe una moneda con el nombre '{nombre}'")
        moneda = Moneda(codigo=codigo, nombre=nombre, simbolo=simbolo, es_base=es_base, tasa_cambio=tasa_cambio)
        return self.repositorio.crear(moneda)


class ListarMonedas:
    def __init__(self, repositorio: RepositorioMoneda):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerMoneda:
    def __init__(self, repositorio: RepositorioMoneda):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Moneda:
        moneda = self.repositorio.obtener_por_id(id)
        if not moneda:
            raise MonedaNoExiste("Moneda no encontrada")
        return moneda


class ActualizarMoneda:
    def __init__(self, repositorio: RepositorioMoneda):
        self.repositorio = repositorio

    def ejecutar(self, id: int, codigo: str = None, nombre: str = None, simbolo: str = None, estado: str = None, es_base: bool = None, tasa_cambio: float = None) -> Moneda:
        moneda = self.repositorio.obtener_por_id(id)
        if not moneda:
            raise MonedaNoExiste("Moneda no encontrada")

        if nombre is not None:
            if self.repositorio.existe_nombre(nombre, excluir_id=id):
                raise MonedaYaExiste(f"Ya existe una moneda con el nombre '{nombre}'")
            moneda.nombre = nombre
        if codigo is not None: moneda.codigo = codigo
        if simbolo is not None: moneda.simbolo = simbolo
        if estado is not None: moneda.estado = EstadoUsuario(estado)
        if es_base is not None: moneda.es_base = es_base
        if tasa_cambio is not None: moneda.tasa_cambio = tasa_cambio
        return self.repositorio.actualizar(moneda)


class EliminarMoneda:
    def __init__(self, repositorio: RepositorioMoneda):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        moneda = self.repositorio.obtener_por_id(id)
        if not moneda:
            raise MonedaNoExiste("Moneda no encontrada")
        return self.repositorio.eliminar(id)
