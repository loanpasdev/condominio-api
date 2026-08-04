from fastapi import APIRouter, Depends, HTTPException
from app.presentacion.esquemas.auth import (
    SolicitudCrearUsuario, SolicitudActualizarUsuario,
    RespuestaUsuario, RespuestaListaUsuarios
)
from app.presentacion.dependencias import obtener_repositorio_usuario, requerir_admin
from app.aplicacion.caso_uso.auth.crud_usuarios import (
    ListarUsuarios, ObtenerUsuario, CrearUsuario,
    ActualizarUsuario, EliminarUsuario
)
from app.dominio.usuario.excepciones import UsuarioYaExiste, UsuarioNoEncontrado

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


@router.get("/", response_model=RespuestaListaUsuarios)
def listar_usuarios(
    usuario_actual = Depends(requerir_admin),
    repositorio = Depends(obtener_repositorio_usuario),
):
    caso_uso = ListarUsuarios(repositorio)
    usuarios = caso_uso.ejecutar()
    return RespuestaListaUsuarios(
        usuarios=[RespuestaUsuario.from_orm_model(u) for u in usuarios],
        total=len(usuarios),
    )


@router.get("/{usuario_id}", response_model=RespuestaUsuario)
def obtener_usuario(
    usuario_id: int,
    usuario_actual = Depends(requerir_admin),
    repositorio = Depends(obtener_repositorio_usuario),
):
    caso_uso = ObtenerUsuario(repositorio)
    try:
        usuario = caso_uso.ejecutar(usuario_id)
        return RespuestaUsuario.from_orm_model(usuario)
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=RespuestaUsuario, status_code=201)
def crear_usuario(
    datos: SolicitudCrearUsuario,
    usuario_actual = Depends(requerir_admin),
    repositorio = Depends(obtener_repositorio_usuario),
):
    caso_uso = CrearUsuario(repositorio)
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
        return RespuestaUsuario.from_orm_model(usuario)
    except UsuarioYaExiste as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{usuario_id}", response_model=RespuestaUsuario)
def actualizar_usuario(
    usuario_id: int,
    datos: SolicitudActualizarUsuario,
    usuario_actual = Depends(requerir_admin),
    repositorio = Depends(obtener_repositorio_usuario),
):
    caso_uso = ActualizarUsuario(repositorio)
    try:
        return caso_uso.ejecutar(
            usuario_id=usuario_id,
            nombre=datos.nombre,
            apellido=datos.apellido,
            telefono=datos.telefono,
            cedula=datos.cedula,
            correo=datos.correo,
            rol=datos.rol,
            estado=datos.estado,
        )
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
    except UsuarioYaExiste as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    usuario_actual = Depends(requerir_admin),
    repositorio = Depends(obtener_repositorio_usuario),
):
    caso_uso = EliminarUsuario(repositorio)
    try:
        caso_uso.ejecutar(usuario_id)
        return {"mensaje": "Usuario eliminado correctamente"}
    except UsuarioNoEncontrado as e:
        raise HTTPException(status_code=404, detail=str(e))
