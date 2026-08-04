from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from app.database import Base
from datetime import datetime


class ProveedorModelo(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    rif = Column(String(20), nullable=False)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    # Valores: 'activo', 'inactivo'
    estado = Column(String(20), default="activo")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
