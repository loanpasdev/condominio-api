from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.database import Base
from datetime import datetime


class SolicitudModelo(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=True)
    propietario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=False)
    categoria = Column(String(50), nullable=False)
    prioridad = Column(String(20), default="media")
    estado = Column(String(20), default="abierta")
    responsable = Column(String(100))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
