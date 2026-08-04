from app.dominio.unidad.entidad import Unidad
from app.dominio.unidad.excepciones import UnidadNoExiste, UnidadYaExiste
from app.puertos.salida.repositorio_unidad import RepositorioUnidad
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearUnidad:
    def __init__(self, repositorio: RepositorioUnidad, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, condominio_id: int, tipo_unidad_id: int, numero: str, metraje: float, porcentual: float, propietario_id: int = None, piso: str = None, grupo_residencial_id: int = None, habitaciones: int = 0, banios: int = 0, terraza: bool = False, balcon: bool = False, parking: bool = False, notas: str = None) -> Unidad:
        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")
        return self.repositorio.crear(Unidad(
            condominio_id=condominio_id, tipo_unidad_id=tipo_unidad_id,
            numero=numero, metraje=metraje, porcentual=porcentual,
            propietario_id=propietario_id, piso=piso,
            grupo_residencial_id=grupo_residencial_id, habitaciones=habitaciones, banios=banios,
            terraza=terraza, balcon=balcon, parking=parking, notas=notas,
        ))


class ListarUnidades:
    def __init__(self, repositorio: RepositorioUnidad):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)


class ObtenerUnidad:
    def __init__(self, repositorio: RepositorioUnidad):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Unidad:
        unidad = self.repositorio.obtener_por_id(id)
        if not unidad:
            raise UnidadNoExiste("Unidad no encontrada")
        return unidad


class ActualizarUnidad:
    def __init__(self, repositorio: RepositorioUnidad, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, id: int, condominio_id: int, tipo_unidad_id: int, numero: str, metraje: float, porcentual: float, propietario_id: int, piso: str, estado: bool = True, grupo_residencial_id: int = None, habitaciones: int = 0, banios: int = 0, terraza: bool = False, balcon: bool = False, parking: bool = False, notas: str = None) -> Unidad:
        unidad = self.repositorio.obtener_por_id(id)
        if not unidad:
            raise UnidadNoExiste("Unidad no encontrada")
        unidad.condominio_id = condominio_id
        unidad.tipo_unidad_id = tipo_unidad_id
        unidad.numero = numero
        unidad.metraje = metraje
        unidad.porcentual = porcentual
        unidad.propietario_id = propietario_id
        unidad.piso = piso
        unidad.grupo_residencial_id = grupo_residencial_id
        unidad.habitaciones = habitaciones
        unidad.banios = banios
        unidad.terraza = terraza
        unidad.balcon = balcon
        unidad.parking = parking
        unidad.notas = notas
        unidad.estado = estado
        return self.repositorio.actualizar(unidad)


class EliminarUnidad:
    def __init__(self, repositorio: RepositorioUnidad):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        unidad = self.repositorio.obtener_por_id(id)
        if not unidad:
            raise UnidadNoExiste("Unidad no encontrada")
        return self.repositorio.eliminar(id)


class DuplicarUnidad:
    def __init__(self, repositorio: RepositorioUnidad):
        self.repositorio = repositorio

    def ejecutar(self, id: int, numero: str) -> Unidad:
        unidad = self.repositorio.obtener_por_id(id)
        if not unidad:
            raise UnidadNoExiste("Unidad no encontrada")
        nueva = Unidad(
            condominio_id=unidad.condominio_id,
            tipo_unidad_id=unidad.tipo_unidad_id,
            numero=numero,
            metraje=unidad.metraje,
            porcentual=unidad.porcentual,
            propietario_id=None,
            piso=unidad.piso,
            grupo_residencial_id=unidad.grupo_residencial_id,
            habitaciones=unidad.habitaciones,
            banios=unidad.banios,
            terraza=unidad.terraza,
            balcon=unidad.balcon,
            parking=unidad.parking,
            notas=unidad.notas,
            estado=unidad.estado,
        )
        return self.repositorio.crear(nueva)
