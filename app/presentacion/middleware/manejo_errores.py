from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


async def manejador_excepciones_http(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "mensaje": exc.detail,
            "codigo_estado": exc.status_code,
        },
    )


async def manejador_excepciones_generales(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "mensaje": "Error interno del servidor",
            "codigo_estado": 500,
        },
    )
