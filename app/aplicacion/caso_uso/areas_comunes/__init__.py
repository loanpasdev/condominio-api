from app.dominio.area_comun.entidad import AreaComun
from app.dominio.area_comun.excepciones import AreaComunNoExiste, AreaComunYaExiste
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_area_comun import RepositorioAreaComun
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearAreaComun:
    def __init__(self, repositorio: RepositorioAreaComun, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, nombre: str, condominio_id: int, descripcion: str = None,
                 capacidad: int = None, tarifa: float = 0,
                 hora_inicio: str = None, hora_fin: str = None) -> AreaComun:
        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id):
            raise AreaComunYaExiste(f"Ya existe un area comun con el nombre '{nombre}' en este condominio")

        area = AreaComun(
            nombre=nombre, condominio_id=condominio_id,
            descripcion=descripcion, capacidad=capacidad,
            tarifa=tarifa, hora_inicio=hora_inicio, hora_fin=hora_fin,
        )
        return self.repositorio.crear(area)


class ListarAreasComunes:
    def __init__(self, repositorio: RepositorioAreaComun):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerAreaComun:
    def __init__(self, repositorio: RepositorioAreaComun):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> AreaComun:
        area = self.repositorio.obtener_por_id(id)
        if not area:
            raise AreaComunNoExiste("Area comun no encontrada")
        return area


class ActualizarAreaComun:
    def __init__(self, repositorio: RepositorioAreaComun, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, id: int, nombre: str, condominio_id: int, descripcion: str,
                 capacidad: int, tarifa: float, hora_inicio: str, hora_fin: str, estado: str) -> AreaComun:
        area = self.repositorio.obtener_por_id(id)
        if not area:
            raise AreaComunNoExiste("Area comun no encontrada")

        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id, excluir_id=id):
            raise AreaComunYaExiste(f"Ya existe otro area comun con el nombre '{nombre}' en este condominio")

        area.nombre = nombre
        area.condominio_id = condominio_id
        area.descripcion = descripcion
        area.capacidad = capacidad
        area.tarifa = tarifa
        area.hora_inicio = hora_inicio
        area.hora_fin = hora_fin
        area.estado = EstadoUsuario(estado)
        return self.repositorio.actualizar(area)


class EliminarAreaComun:
    def __init__(self, repositorio: RepositorioAreaComun):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        area = self.repositorio.obtener_por_id(id)
        if not area:
            raise AreaComunNoExiste("Area comun no encontrada")
        return self.repositorio.eliminar(id)
