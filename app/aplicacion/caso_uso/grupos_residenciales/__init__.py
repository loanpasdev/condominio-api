from app.dominio.grupo_residencial import GrupoResidencial
from app.dominio.grupo_residencial.excepciones import GrupoResidencialNoExiste, GrupoResidencialYaExiste
from app.puertos.salida.repositorio_grupo_residencial import RepositorioGrupoResidencial
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearGrupoResidencial:
    def __init__(self, repositorio: RepositorioGrupoResidencial, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, condominio_id: int, nombre: str, descripcion: str = None) -> GrupoResidencial:
        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id):
            raise GrupoResidencialYaExiste(f"Ya existe un grupo residencial con el nombre '{nombre}' en este condominio")

        grupo = GrupoResidencial(condominio_id=condominio_id, nombre=nombre, descripcion=descripcion)
        return self.repositorio.crear(grupo)


class ListarGruposResidenciales:
    def __init__(self, repositorio: RepositorioGrupoResidencial):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)


class ObtenerGrupoResidencial:
    def __init__(self, repositorio: RepositorioGrupoResidencial):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> GrupoResidencial:
        grupo = self.repositorio.obtener_por_id(id)
        if not grupo:
            raise GrupoResidencialNoExiste("Grupo residencial no encontrado")
        return grupo


class ActualizarGrupoResidencial:
    def __init__(self, repositorio: RepositorioGrupoResidencial, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, id: int, nombre: str, descripcion: str = None, estado: bool = True) -> GrupoResidencial:
        grupo = self.repositorio.obtener_por_id(id)
        if not grupo:
            raise GrupoResidencialNoExiste("Grupo residencial no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, grupo.condominio_id, excluir_id=id):
            raise GrupoResidencialYaExiste(f"Ya existe otro grupo residencial con el nombre '{nombre}' en este condominio")

        grupo.nombre = nombre
        grupo.descripcion = descripcion
        grupo.estado = estado
        return self.repositorio.actualizar(grupo)


class EliminarGrupoResidencial:
    def __init__(self, repositorio: RepositorioGrupoResidencial):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        grupo = self.repositorio.obtener_por_id(id)
        if not grupo:
            raise GrupoResidencialNoExiste("Grupo residencial no encontrado")
        return self.repositorio.eliminar(id)
