from app.dominio.cuota.entidad import Cuota
from app.dominio.cuota.excepciones import CuotaNoExiste
from app.puertos.salida.repositorio_cuota import RepositorioCuota
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearCuota:
    def __init__(self, repositorio: RepositorioCuota, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, condominio_id: int = None, unidad_id: int = None, mes: int = None, anio: int = None, monto_total: float = 0) -> Cuota:
        return self.repositorio.crear(Cuota(
            condominio_id=condominio_id or 1, unidad_id=unidad_id,
            mes=mes, anio=anio, monto_total=monto_total,
        ))


class ListarCuotas:
    def __init__(self, repositorio: RepositorioCuota):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, unidad_id: int = None, mes: int = None, anio: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, unidad_id=unidad_id, mes=mes, anio=anio, pagina=pagina, por_pagina=por_pagina)


class ObtenerCuota:
    def __init__(self, repositorio: RepositorioCuota):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Cuota:
        cuota = self.repositorio.obtener_por_id(id)
        if not cuota:
            raise CuotaNoExiste("Cuota no encontrada")
        return cuota


class ActualizarCuota:
    def __init__(self, repositorio: RepositorioCuota):
        self.repositorio = repositorio

    def ejecutar(self, id: int, monto_total: float = None, estado: str = None) -> Cuota:
        cuota = self.repositorio.obtener_por_id(id)
        if not cuota:
            raise CuotaNoExiste("Cuota no encontrada")
        if monto_total is not None: cuota.monto_total = monto_total
        if estado is not None: cuota.estado = estado
        return self.repositorio.actualizar(cuota)


class EliminarCuota:
    def __init__(self, repositorio: RepositorioCuota):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        cuota = self.repositorio.obtener_por_id(id)
        if not cuota:
            raise CuotaNoExiste("Cuota no encontrada")
        return self.repositorio.eliminar(id)
