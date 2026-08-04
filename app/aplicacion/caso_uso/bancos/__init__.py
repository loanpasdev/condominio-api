from app.dominio.banco.entidad import Banco
from app.dominio.banco.excepciones import BancoNoExiste, BancoYaExiste
from app.puertos.salida.repositorio_banco import RepositorioBanco


class CrearBanco:
    def __init__(self, repositorio: RepositorioBanco):
        self.repositorio = repositorio

    def ejecutar(self, codigo: str, nombre: str) -> Banco:
        if self.repositorio.existe_nombre(nombre):
            raise BancoYaExiste(f"Ya existe un banco con el nombre '{nombre}'")
        banco = Banco(codigo=codigo, nombre=nombre)
        return self.repositorio.crear(banco)


class ListarBancos:
    def __init__(self, repositorio: RepositorioBanco):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerBanco:
    def __init__(self, repositorio: RepositorioBanco):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Banco:
        banco = self.repositorio.obtener_por_id(id)
        if not banco:
            raise BancoNoExiste("Banco no encontrado")
        return banco


class ActualizarBanco:
    def __init__(self, repositorio: RepositorioBanco):
        self.repositorio = repositorio

    def ejecutar(self, id: int, codigo: str, nombre: str) -> Banco:
        banco = self.repositorio.obtener_por_id(id)
        if not banco:
            raise BancoNoExiste("Banco no encontrado")

        if self.repositorio.existe_nombre(nombre, excluir_id=id):
            raise BancoYaExiste(f"Ya existe un banco con el nombre '{nombre}'")

        banco.codigo = codigo
        banco.nombre = nombre
        return self.repositorio.actualizar(banco)


class EliminarBanco:
    def __init__(self, repositorio: RepositorioBanco):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        banco = self.repositorio.obtener_por_id(id)
        if not banco:
            raise BancoNoExiste("Banco no encontrado")
        return self.repositorio.eliminar(id)
