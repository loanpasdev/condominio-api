from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text, Date, Time
from app.database import Base
from datetime import datetime


class AsambleaModelo(Base):
    __tablename__ = "asambleas"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=True)
    tipo = Column(String(20), nullable=False)
    titulo = Column(String(200), nullable=False)
    descripcion = Column(Text)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    lugar = Column(String(200))
    quorum_requerido = Column(Numeric(5, 2), nullable=False)
    quorum_obtenido = Column(Numeric(5, 2), default=0)
    estado = Column(String(20), default="programada")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
