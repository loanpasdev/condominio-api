from app.dominio.metodo_pago.entidad import MetodoPago
from app.dominio.metodo_pago.excepciones import MetodoPagoNoExiste, MetodoPagoYaExiste
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_metodo_pago import RepositorioMetodoPago
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearMetodoPago:
    def __init__(self, repositorio: RepositorioMetodoPago, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, nombre: str, condominio_id: int) -> MetodoPago:
        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id):
            raise MetodoPagoYaExiste(f"Ya existe un metodo de pago con el nombre '{nombre}' en este condominio")

        metodo_pago = MetodoPago(nombre=nombre, condominio_id=condominio_id)
        return self.repositorio.crear(metodo_pago)


class ListarMetodosPago:
    def __init__(self, repositorio: RepositorioMetodoPago):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerMetodoPago:
    def __init__(self, repositorio: RepositorioMetodoPago):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> MetodoPago:
        metodo = self.repositorio.obtener_por_id(id)
        if not metodo:
            raise MetodoPagoNoExiste("Método de pago no encontrado")
        return metodo


class ActualizarMetodoPago:
    def __init__(self, repositorio: RepositorioMetodoPago, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, id: int, nombre: str, condominio_id: int, estado: str) -> MetodoPago:
        metodo = self.repositorio.obtener_por_id(id)
        if not metodo:
            raise MetodoPagoNoExiste("Método de pago no encontrado")

        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id, excluir_id=id):
            raise MetodoPagoYaExiste(f"Ya existe otro metodo de pago con el nombre '{nombre}' en este condominio")

        metodo.nombre = nombre
        metodo.condominio_id = condominio_id
        metodo.estado = EstadoUsuario(estado)
        return self.repositorio.actualizar(metodo)


class EliminarMetodoPago:
    def __init__(self, repositorio: RepositorioMetodoPago):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        metodo = self.repositorio.obtener_por_id(id)
        if not metodo:
            raise MetodoPagoNoExiste("Método de pago no encontrado")
        return self.repositorio.eliminar(id)
