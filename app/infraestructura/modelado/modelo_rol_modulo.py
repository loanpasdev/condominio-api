from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime


class RolModuloModelo(Base):
    __tablename__ = "rol_modulo"

    id = Column(Integer, primary_key=True, index=True)
    rol = Column(String(20), nullable=False)
    modulo_id = Column(Integer, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
