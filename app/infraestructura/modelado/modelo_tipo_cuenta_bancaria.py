from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base
from datetime import datetime


class TipoCuentaBancariaModelo(Base):
    __tablename__ = "tipos_cuenta_bancaria"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=False)
    # Valores: 'activo', 'inactivo'
    estado = Column(String(20), default="activo")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
