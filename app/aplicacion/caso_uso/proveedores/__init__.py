from app.dominio.proveedor.entidad import Proveedor
from app.dominio.proveedor.excepciones import ProveedorNoExiste, ProveedorYaExiste
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_proveedor import RepositorioProveedor
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearProveedor:
    def __init__(self, repositorio: RepositorioProveedor, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, nombre: str, rif: str, condominio_id: int, telefono: str = None, email: str = None) -> Proveedor:
        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id):
            raise ProveedorYaExiste(f"Ya existe un proveedor con el nombre '{nombre}' en este condominio")

        proveedor = Proveedor(
            nombre=nombre, rif=rif, condominio_id=condominio_id,
            telefono=telefono, email=email,
        )
        return self.repositorio.crear(proveedor)


class ListarProveedores:
    def __init__(self, repositorio: RepositorioProveedor):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerProveedor:
    def __init__(self, repositorio: RepositorioProveedor):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Proveedor:
        proveedor = self.repositorio.obtener_por_id(id)
        if not proveedor:
            raise ProveedorNoExiste("Proveedor no encontrado")
        return proveedor


class ActualizarProveedor:
    def __init__(self, repositorio: RepositorioProveedor, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, id: int, nombre: str, rif: str, condominio_id: int, telefono: str, email: str, estado: str) -> Proveedor:
        proveedor = self.repositorio.obtener_por_id(id)
        if not proveedor:
            raise ProveedorNoExiste("Proveedor no encontrado")

        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id, excluir_id=id):
            raise ProveedorYaExiste(f"Ya existe otro proveedor con el nombre '{nombre}' en este condominio")

        proveedor.nombre = nombre
        proveedor.rif = rif
        proveedor.condominio_id = condominio_id
        proveedor.telefono = telefono
        proveedor.email = email
        proveedor.estado = EstadoUsuario(estado)
        return self.repositorio.actualizar(proveedor)


class EliminarProveedor:
    def __init__(self, repositorio: RepositorioProveedor):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        proveedor = self.repositorio.obtener_por_id(id)
        if not proveedor:
            raise ProveedorNoExiste("Proveedor no encontrado")
        return self.repositorio.eliminar(id)
