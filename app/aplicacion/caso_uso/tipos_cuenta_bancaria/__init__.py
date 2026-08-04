from app.dominio.tipo_cuenta_bancaria.entidad import TipoCuentaBancaria
from app.dominio.tipo_cuenta_bancaria.excepciones import TipoCuentaBancariaNoExiste, TipoCuentaBancariaYaExiste
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_tipo_cuenta_bancaria import RepositorioTipoCuentaBancaria
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearTipoCuentaBancaria:
    def __init__(self, repositorio: RepositorioTipoCuentaBancaria, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, nombre: str, condominio_id: int) -> TipoCuentaBancaria:
        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id):
            raise TipoCuentaBancariaYaExiste(f"Ya existe un tipo de cuenta bancaria con el nombre '{nombre}' en este condominio")

        tipo_cuenta = TipoCuentaBancaria(
            nombre=nombre,
            condominio_id=condominio_id,
        )
        return self.repositorio.crear(tipo_cuenta)


class ListarTiposCuentaBancaria:
    def __init__(self, repositorio: RepositorioTipoCuentaBancaria):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerTipoCuentaBancaria:
    def __init__(self, repositorio: RepositorioTipoCuentaBancaria):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> TipoCuentaBancaria:
        tipo_cuenta = self.repositorio.obtener_por_id(id)
        if not tipo_cuenta:
            raise TipoCuentaBancariaNoExiste("Tipo de cuenta bancaria no encontrado")
        return tipo_cuenta


class ActualizarTipoCuentaBancaria:
    def __init__(self, repositorio: RepositorioTipoCuentaBancaria, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, id: int, nombre: str, condominio_id: int, estado: str) -> TipoCuentaBancaria:
        tipo_cuenta = self.repositorio.obtener_por_id(id)
        if not tipo_cuenta:
            raise TipoCuentaBancariaNoExiste("Tipo de cuenta bancaria no encontrado")

        condominio = self.repositorio_condominio.obtener_por_id(condominio_id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        if self.repositorio.existe_nombre_en_condominio(nombre, condominio_id, excluir_id=id):
            raise TipoCuentaBancariaYaExiste(f"Ya existe otro tipo de cuenta bancaria con el nombre '{nombre}' en este condominio")

        tipo_cuenta.nombre = nombre
        tipo_cuenta.condominio_id = condominio_id
        tipo_cuenta.estado = EstadoUsuario(estado)
        return self.repositorio.actualizar(tipo_cuenta)


class EliminarTipoCuentaBancaria:
    def __init__(self, repositorio: RepositorioTipoCuentaBancaria):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        tipo_cuenta = self.repositorio.obtener_por_id(id)
        if not tipo_cuenta:
            raise TipoCuentaBancariaNoExiste("Tipo de cuenta bancaria no encontrado")
        return self.repositorio.eliminar(id)
