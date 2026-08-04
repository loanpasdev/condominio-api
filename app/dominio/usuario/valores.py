from enum import Enum


class RolUsuario(str, Enum):
    ADMIN = "admin"
    PRESIDENTE = "presidente"
    TESORERA = "tesorera"
    SECRETARIO = "secretario"
    PROPIETARIO = "propietario"
    CONSEJO = "consejo"


class EstadoUsuario(str, Enum):
    ACTIVO = "activo"
    INACTIVO = "inactivo"
