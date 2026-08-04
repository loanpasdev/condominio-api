from app.dominio.propietario.entidad import Propietario
from app.dominio.propietario.excepciones import PropietarioNoExiste, PropietarioYaExiste
from app.puertos.salida.repositorio_propietario import RepositorioPropietario


class ListarPropietarios:
    def __init__(self, repositorio: RepositorioPropietario):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, estado: bool = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, estado=estado, pagina=pagina, por_pagina=por_pagina)


class ObtenerPropietario:
    def __init__(self, repositorio: RepositorioPropietario):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> Propietario:
        propietario = self.repositorio.obtener_por_id(id)
        if not propietario:
            raise PropietarioNoExiste("Propietario no encontrado")
        return propietario


class CrearPropietario:
    def __init__(self, repositorio: RepositorioPropietario):
        self.repositorio = repositorio

    def ejecutar(self, condominio_id: int, nombre: str, apellido: str, cedula: str, correo: str, telefono: str = None, direccion: str = None, usuario_id: int = None) -> Propietario:
        if self.repositorio.existe_por_cedula(cedula):
            raise PropietarioYaExiste(f"Ya existe un propietario con cedula {cedula}")
        return self.repositorio.crear(Propietario(
            condominio_id=condominio_id, nombre=nombre, apellido=apellido,
            cedula=cedula, correo=correo, telefono=telefono,
            direccion=direccion, usuario_id=usuario_id,
        ))


class ActualizarPropietario:
    def __init__(self, repositorio: RepositorioPropietario):
        self.repositorio = repositorio

    def ejecutar(self, id: int, condominio_id: int = None, nombre: str = None, apellido: str = None, cedula: str = None, correo: str = None, telefono: str = None, direccion: str = None, estado: bool = None, usuario_id: int = None) -> Propietario:
        propietario = self.repositorio.obtener_por_id(id)
        if not propietario:
            raise PropietarioNoExiste("Propietario no encontrado")
        if cedula and cedula != propietario.cedula and self.repositorio.existe_por_cedula(cedula, exclude_id=id):
            raise PropietarioYaExiste(f"Ya existe un propietario con cedula {cedula}")
        if condominio_id is not None: propietario.condominio_id = condominio_id
        if nombre is not None: propietario.nombre = nombre
        if apellido is not None: propietario.apellido = apellido
        if cedula is not None: propietario.cedula = cedula
        if correo is not None: propietario.correo = correo
        if telefono is not None: propietario.telefono = telefono
        if direccion is not None: propietario.direccion = direccion
        if estado is not None: propietario.estado = estado
        if usuario_id is not None: propietario.usuario_id = usuario_id
        return self.repositorio.actualizar(propietario)


class EliminarPropietario:
    def __init__(self, repositorio: RepositorioPropietario):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        propietario = self.repositorio.obtener_por_id(id)
        if not propietario:
            raise PropietarioNoExiste("Propietario no encontrado")
        return self.repositorio.eliminar(id)
