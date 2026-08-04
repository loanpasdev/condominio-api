from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric, Time
from app.database import Base
from datetime import datetime


class AreaComunModelo(Base):
    __tablename__ = "areas_comunes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=False)
    descripcion = Column(Text)
    capacidad = Column(Integer)
    tarifa = Column(Numeric(10, 2), default=0)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    # Valores: 'activo', 'inactivo'
    estado = Column(String(20), default="activo")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
