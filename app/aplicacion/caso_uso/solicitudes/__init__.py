from app.dominio.solicitud.entidad import Solicitud
from app.dominio.solicitud.excepciones import SolicitudNoExiste
from app.puertos.salida.repositorio_solicitud import RepositorioSolicitud


class CrearSolicitud:
    def __init__(self, repositorio: RepositorioSolicitud):
        self.repositorio = repositorio

    def ejecutar(self, condominio_id: int = None, propietario_id: int = None, titulo: str = '', descripcion: str = '', categoria: str = 'otro', prioridad: str = "media", responsable: str = None) -> Solicitud:
        return self.repositorio.crear(Solicitud(
            condominio_id=condominio_id or 1, propietario_id=propietario_id,
            titulo=titulo, descripcion=descripcion, categoria=categoria,
            prioridad=prioridad, responsable=responsable,
        ))


class ListarSolicitudes:
    def __init__(self, repositorio: RepositorioSolicitud):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, propietario_id: int = None, estado: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, propietario_id=propietario_id, estado=estado, pagina=pagina, por_pagina=por_pagina)


class ObtenerSolicitud:
    def __init__(self, repositorio: RepositorioSolicitud):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Solicitud:
        solicitud = self.repositorio.obtener_por_id(id)
        if not solicitud:
            raise SolicitudNoExiste("Solicitud no encontrada")
        return solicitud


class ActualizarSolicitud:
    def __init__(self, repositorio: RepositorioSolicitud):
        self.repositorio = repositorio

    def ejecutar(self, id: int, titulo: str = None, descripcion: str = None, categoria: str = None, prioridad: str = None, estado: str = None, responsable: str = None) -> Solicitud:
        solicitud = self.repositorio.obtener_por_id(id)
        if not solicitud:
            raise SolicitudNoExiste("Solicitud no encontrada")
        if titulo is not None: solicitud.titulo = titulo
        if descripcion is not None: solicitud.descripcion = descripcion
        if categoria is not None: solicitud.categoria = categoria
        if prioridad is not None: solicitud.prioridad = prioridad
        if estado is not None: solicitud.estado = estado
        if responsable is not None: solicitud.responsable = responsable
        return self.repositorio.actualizar(solicitud)


class EliminarSolicitud:
    def __init__(self, repositorio: RepositorioSolicitud):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        solicitud = self.repositorio.obtener_por_id(id)
        if not solicitud:
            raise SolicitudNoExiste("Solicitud no encontrada")
        return self.repositorio.eliminar(id)
