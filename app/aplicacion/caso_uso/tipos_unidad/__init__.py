from app.dominio.tipo_unidad.entidad import TipoUnidad
from app.dominio.tipo_unidad.excepciones import TipoUnidadNoExiste, TipoUnidadYaExiste
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_tipo_unidad import RepositorioTipoUnidad
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearTipoUnidad:
    def __init__(self, repositorio: RepositorioTipoUnidad, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, nombre: str, condominio_id: int) -> TipoUnidad:
        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id):
            raise TipoUnidadYaExiste(f"Ya existe un tipo de unidad con el nombre '{nombre}' en este condominio")

        tipo_unidad = TipoUnidad(
            nombre=nombre,
            condominio_id=condominio_id,
        )
        return self.repositorio.crear(tipo_unidad)


class ListarTiposUnidad:
    def __init__(self, repositorio: RepositorioTipoUnidad):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerTipoUnidad:
    def __init__(self, repositorio: RepositorioTipoUnidad):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> TipoUnidad:
        tipo_unidad = self.repositorio.obtener_por_id(id)
        if not tipo_unidad:
            raise TipoUnidadNoExiste("Tipo de unidad no encontrado")
        return tipo_unidad


class ActualizarTipoUnidad:
    def __init__(self, repositorio: RepositorioTipoUnidad, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, id: int, nombre: str, condominio_id: int, estado: str) -> TipoUnidad:
        tipo_unidad = self.repositorio.obtener_por_id(id)
        if not tipo_unidad:
            raise TipoUnidadNoExiste("Tipo de unidad no encontrado")

        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id, excluir_id=id):
            raise TipoUnidadYaExiste(f"Ya existe otro tipo de unidad con el nombre '{nombre}' en este condominio")

        tipo_unidad.nombre = nombre
        tipo_unidad.condominio_id = condominio_id
        tipo_unidad.estado = EstadoUsuario(estado)
        return self.repositorio.actualizar(tipo_unidad)


class EliminarTipoUnidad:
    def __init__(self, repositorio: RepositorioTipoUnidad):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        tipo_unidad = self.repositorio.obtener_por_id(id)
        if not tipo_unidad:
            raise TipoUnidadNoExiste("Tipo de unidad no encontrado")
        return self.repositorio.eliminar(id)
