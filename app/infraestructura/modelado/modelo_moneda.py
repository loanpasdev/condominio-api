from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric
from app.database import Base
from datetime import datetime


class MonedaModelo(Base):
    __tablename__ = "monedas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(3), unique=True, nullable=False)
    nombre = Column(String(50), nullable=False)
    simbolo = Column(String(5), nullable=False)
    estado = Column(String(20), default="activo")
    es_base = Column(Boolean, default=False)
    tasa_cambio = Column(Numeric(15, 6), default=1.0)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
