from pydantic_settings import BaseSettings
from typing import List


class Configuracion(BaseSettings):
    DATABASE_URL: str
    CLAVE_SECRETA: str
    ALGORITMO: str = "HS256"
    MINUTOS_EXPIRACION_TOKEN: int = 30
    ORIGENES_CORS: List[str] = ["http://localhost:5173", "http://localhost:5174"]

    class Config:
        env_file = ".env"


configuracion = Configuracion()
