from app.dominio.notificacion.entidad import Notificacion
from app.dominio.notificacion.excepciones import NotificacionNoExiste
from app.puertos.salida.repositorio_notificacion import RepositorioNotificacion


class CrearNotificacion:
    def __init__(self, repositorio: RepositorioNotificacion):
        self.repositorio = repositorio

    def ejecutar(self, condominio_id: int, titulo: str, mensaje: str, tipo: str, usuario_id: int = None) -> Notificacion:
        return self.repositorio.crear(Notificacion(
            condominio_id=condominio_id, titulo=titulo,
            mensaje=mensaje, tipo=tipo, usuario_id=usuario_id,
        ))


class ListarNotificaciones:
    def __init__(self, repositorio: RepositorioNotificacion):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, usuario_id: int = None, tipo: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, usuario_id=usuario_id, tipo=tipo, pagina=pagina, por_pagina=por_pagina)


class ObtenerNotificacion:
    def __init__(self, repositorio: RepositorioNotificacion):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Notificacion:
        notificacion = self.repositorio.obtener_por_id(id)
        if not notificacion:
            raise NotificacionNoExiste("Notificacion no encontrada")
        return notificacion


class ActualizarNotificacion:
    def __init__(self, repositorio: RepositorioNotificacion):
        self.repositorio = repositorio

    def ejecutar(self, id: int, titulo: str, mensaje: str, tipo: str, leida: bool) -> Notificacion:
        notificacion = self.repositorio.obtener_por_id(id)
        if not notificacion:
            raise NotificacionNoExiste("Notificacion no encontrada")
        notificacion.titulo = titulo
        notificacion.mensaje = mensaje
        notificacion.tipo = tipo
        notificacion.leida = leida
        return self.repositorio.actualizar(notificacion)


class EliminarNotificacion:
    def __init__(self, repositorio: RepositorioNotificacion):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        notificacion = self.repositorio.obtener_por_id(id)
        if not notificacion:
            raise NotificacionNoExiste("Notificacion no encontrada")
        return self.repositorio.eliminar(id)
