from pydantic import BaseModel, EmailStr
from typing import Optional, List


class SolicitudLogin(BaseModel):
    correo: str
    contrasena: str


class SolicitudRegistro(BaseModel):
    correo: str
    contrasena: str
    nombre: str
    apellido: Optional[str] = None
    rol: str = "propietario"


class SolicitudCambiarContrasena(BaseModel):
    contrasena_actual: str
    contrasena_nueva: str


class SolicitudActualizarPerfil(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    cedula: Optional[str] = None


class RespuestaUsuario(BaseModel):
    id: int
    correo: str
    nombre: str
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    cedula: Optional[str] = None
    rol: str
    estado: str = "activo"
    ultimo_acceso: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_model(cls, obj):
        ultimo = None
        if hasattr(obj, 'ultimo_acceso') and obj.ultimo_acceso:
            ultimo = obj.ultimo_acceso.strftime('%d/%m/%Y %H:%M')
        return cls(
            id=obj.id,
            correo=obj.correo,
            nombre=obj.nombre,
            apellido=getattr(obj, 'apellido', None),
            telefono=getattr(obj, 'telefono', None),
            cedula=getattr(obj, 'cedula', None),
            rol=obj.rol if isinstance(obj.rol, str) else obj.rol.value,
            estado=obj.estado if isinstance(obj.estado, str) else obj.estado.value,
            ultimo_acceso=ultimo,
        )


class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str
    usuario: RespuestaUsuario
    modulos: List[str] = []


class SolicitudCrearUsuario(BaseModel):
    correo: str
    contrasena: str
    nombre: str
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    cedula: Optional[str] = None
    rol: str = "propietario"


class SolicitudActualizarUsuario(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    cedula: Optional[str] = None
    correo: Optional[str] = None
    rol: Optional[str] = None
    estado: Optional[str] = None


class RespuestaListaUsuarios(BaseModel):
    usuarios: List[RespuestaUsuario]
    total: int
