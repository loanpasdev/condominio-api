from app.dominio.categoria_gasto.entidad import CategoriaGasto
from app.dominio.categoria_gasto.excepciones import CategoriaGastoNoExiste, CategoriaGastoYaExiste
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_categoria_gasto import RepositorioCategoriaGasto
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearCategoriaGasto:
    def __init__(self, repositorio: RepositorioCategoriaGasto, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, nombre: str, condominio_id: int) -> CategoriaGasto:
        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id):
            raise CategoriaGastoYaExiste(f"Ya existe una categoria de gasto con el nombre '{nombre}' en este condominio")

        categoria = CategoriaGasto(nombre=nombre, condominio_id=condominio_id)
        return self.repositorio.crear(categoria)


class ListarCategoriasGasto:
    def __init__(self, repositorio: RepositorioCategoriaGasto):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerCategoriaGasto:
    def __init__(self, repositorio: RepositorioCategoriaGasto):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> CategoriaGasto:
        categoria = self.repositorio.obtener_por_id(id)
        if not categoria:
            raise CategoriaGastoNoExiste("Categoria de gasto no encontrada")
        return categoria


class ActualizarCategoriaGasto:
    def __init__(self, repositorio: RepositorioCategoriaGasto, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, id: int, nombre: str, condominio_id: int, estado: str) -> CategoriaGasto:
        categoria = self.repositorio.obtener_por_id(id)
        if not categoria:
            raise CategoriaGastoNoExiste("Categoria de gasto no encontrada")

        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id, excluir_id=id):
            raise CategoriaGastoYaExiste(f"Ya existe otra categoria de gasto con el nombre '{nombre}' en este condominio")

        categoria.nombre = nombre
        categoria.condominio_id = condominio_id
        categoria.estado = EstadoUsuario(estado)
        return self.repositorio.actualizar(categoria)


class EliminarCategoriaGasto:
    def __init__(self, repositorio: RepositorioCategoriaGasto):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        categoria = self.repositorio.obtener_por_id(id)
        if not categoria:
            raise CategoriaGastoNoExiste("Categoria de gasto no encontrada")
        return self.repositorio.eliminar(id)
