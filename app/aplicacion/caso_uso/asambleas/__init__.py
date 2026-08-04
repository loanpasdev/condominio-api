from app.dominio.asamblea.entidad import Asamblea
from app.dominio.asamblea.excepciones import AsambleaNoExiste
from app.puertos.salida.repositorio_asamblea import RepositorioAsamblea


class CrearAsamblea:
    def __init__(self, repositorio: RepositorioAsamblea):
        self.repositorio = repositorio

    def ejecutar(self, condominio_id: int = None, tipo: str = 'ordinaria', titulo: str = '', fecha=None, hora=None, quorum_requerido: float = 0, descripcion: str = None, lugar: str = None) -> Asamblea:
        return self.repositorio.crear(Asamblea(
            condominio_id=condominio_id or 1, tipo=tipo, titulo=titulo,
            fecha=fecha, hora=hora, quorum_requerido=quorum_requerido,
            descripcion=descripcion, lugar=lugar,
        ))


class ListarAsambleas:
    def __init__(self, repositorio: RepositorioAsamblea):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)


class ObtenerAsamblea:
    def __init__(self, repositorio: RepositorioAsamblea):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Asamblea:
        asamblea = self.repositorio.obtener_por_id(id)
        if not asamblea:
            raise AsambleaNoExiste("Asamblea no encontrada")
        return asamblea


class ActualizarAsamblea:
    def __init__(self, repositorio: RepositorioAsamblea):
        self.repositorio = repositorio

    def ejecutar(self, id: int, titulo: str = None, descripcion: str = None, fecha=None, hora=None, lugar: str = None, quorum_requerido: float = None, quorum_obtenido: float = None, estado: str = None) -> Asamblea:
        asamblea = self.repositorio.obtener_por_id(id)
        if not asamblea:
            raise AsambleaNoExiste("Asamblea no encontrada")
        if titulo is not None: asamblea.titulo = titulo
        if descripcion is not None: asamblea.descripcion = descripcion
        if fecha is not None: asamblea.fecha = fecha
        if hora is not None: asamblea.hora = hora
        if lugar is not None: asamblea.lugar = lugar
        if quorum_requerido is not None: asamblea.quorum_requerido = quorum_requerido
        if quorum_obtenido is not None: asamblea.quorum_obtenido = quorum_obtenido
        if estado is not None: asamblea.estado = estado
        return self.repositorio.actualizar(asamblea)


class EliminarAsamblea:
    def __init__(self, repositorio: RepositorioAsamblea):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        asamblea = self.repositorio.obtener_por_id(id)
        if not asamblea:
            raise AsambleaNoExiste("Asamblea no encontrada")
        return self.repositorio.eliminar(id)
