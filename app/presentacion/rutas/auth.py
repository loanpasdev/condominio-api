from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import obtener_db
from app.presentacion.esquemas.auth import (
    SolicitudLogin, SolicitudRegistro, SolicitudCambiarContrasena,
    SolicitudActualizarPerfil, TokenRespuesta, RespuestaUsuario
)
from app.presentacion.dependencias import obtener_repositorio_usuario, obtener_usuario_actual
from app.aplicacion.caso_uso.auth.iniciar_sesion import (
    IniciarSesion, RegistrarUsuario, ObtenerUsuarioActual,
    CambiarContrasena, ActualizarPerfil
)
from app.infraestructura.repositorios.repositorio_permiso_sqlalchemy import RepositorioPermisoSQLAlchemy
from app.dominio.usuario.excepciones import CredencialesInvalidas, UsuarioYaExiste

router = APIRouter(prefix="/api/auth", tags=["Autenticacion"])


@router.post("/iniciar-sesion", response_model=TokenRespuesta)
def iniciar_sesion(
    datos: SolicitudLogin,
    repositorio = Depends(obtener_repositorio_usuario),
    db: Session = Depends(obtener_db),
):
    repositorio_permiso = RepositorioPermisoSQLAlchemy(db)
    caso_uso = IniciarSesion(repositorio, repositorio_permiso)
    try:
        resultado = caso_uso.ejecutar(datos.correo, datos.contrasena)
        return resultado
    except CredencialesInvalidas as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/registrar", response_model=RespuestaUsuario)
def registrar_usuario(
    datos: SolicitudRegistro,
    repositorio = Depends(obtener_repositorio_usuario),
):
    caso_uso = RegistrarUsuario(repositorio)
    try:
        usuario = caso_uso.ejecutar(
            correo=datos.correo,
            contrasena=datos.contrasena,
            nombre=datos.nombre,
            apellido=datos.apellido,
            telefono=datos.telefono,
            cedula=datos.cedula,
            rol=datos.rol,
        )
        return usuario
    except UsuarioYaExiste as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/actual", response_model=RespuestaUsuario)
def obtener_usuario(
    usuario_actual = Depends(obtener_usuario_actual),
):
    return usuario_actual


@router.put("/actualizar-perfil", response_model=RespuestaUsuario)
def actualizar_perfil(
    datos: SolicitudActualizarPerfil,
    usuario_actual = Depends(obtener_usuario_actual),
    repositorio = Depends(obtener_repositorio_usuario),
):
    caso_uso = ActualizarPerfil(repositorio)
    try:
        usuario = caso_uso.ejecutar(
            usuario_id=usuario_actual.id,
            nombre=datos.nombre,
            apellido=datos.apellido,
            telefono=datos.telefono,
            cedula=datos.cedula,
        )
        return usuario
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/cambiar-contrasena")
def cambiar_contrasena(
    datos: SolicitudCambiarContrasena,
    usuario_actual = Depends(obtener_usuario_actual),
    repositorio = Depends(obtener_repositorio_usuario),
):
    caso_uso = CambiarContrasena(repositorio)
    try:
        caso_uso.ejecutar(
            usuario_id=usuario_actual.id,
            contrasena_actual=datos.contrasena_actual,
            contrasena_nueva=datos.contrasena_nueva,
        )
        return {"mensaje": "Contraseña actualizada correctamente"}
    except CredencialesInvalidas as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
