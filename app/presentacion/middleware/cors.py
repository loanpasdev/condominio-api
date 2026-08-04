from fastapi.middleware.cors import CORSMiddleware
from app.config import configuracion


def configurar_cors(aplicacion):
    aplicacion.add_middleware(
        CORSMiddleware,
        allow_origins=configuracion.ORIGENES_CORS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
