from app.dominio.condominio.entidad import Condominio
from app.dominio.condominio.excepciones import CondominioNoExiste, CondominioYaExiste
from app.puertos.salida.repositorio_condominio import RepositorioCondominio


class CrearCondominio:
    def __init__(self, repositorio: RepositorioCondominio):
        self.repositorio = repositorio

    def ejecutar(self, nombre: str, rif: str, direccion: str, telefono: str = None, email: str = None, logo: str = None) -> Condominio:
        existente = self.repositorio.obtener_por_rif(rif)
        if existente:
            raise CondominioYaExiste(f"Ya existe un condominio con RIF {rif}")

        condominio = Condominio(
            nombre=nombre,
            rif=rif,
            direccion=direccion,
            telefono=telefono,
            email=email,
            logo=logo,
        )
        return self.repositorio.crear(condominio)


class ListarCondominios:
    def __init__(self, repositorio: RepositorioCondominio):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerCondominio:
    def __init__(self, repositorio: RepositorioCondominio):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Condominio:
        condominio = self.repositorio.obtener_por_id(id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")
        return condominio


class ActualizarCondominio:
    def __init__(self, repositorio: RepositorioCondominio):
        self.repositorio = repositorio

    def ejecutar(self, id: int, nombre: str, rif: str, direccion: str, telefono: str = None, email: str = None, logo: str = None) -> Condominio:
        condominio = self.repositorio.obtener_por_id(id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")

        existente = self.repositorio.obtener_por_rif(rif)
        if existente and existente.id != id:
            raise CondominioYaExiste(f"Ya existe otro condominio con RIF {rif}")

        condominio.nombre = nombre
        condominio.rif = rif
        condominio.direccion = direccion
        condominio.telefono = telefono
        condominio.email = email
        condominio.logo = logo
        return self.repositorio.actualizar(condominio)


class EliminarCondominio:
    def __init__(self, repositorio: RepositorioCondominio):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        condominio = self.repositorio.obtener_por_id(id)
        if not condominio:
            raise CondominioNoExiste("Condominio no encontrado")
        return self.repositorio.eliminar(id)
