from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text, Date
from app.database import Base
from datetime import datetime


class FacturaModelo(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=False)
    numero = Column(String(20), nullable=False)
    descripcion = Column(Text, nullable=False)
    monto_total = Column(Numeric(10, 2), nullable=False)
    fecha = Column(Date, nullable=False)
    distribucion = Column(String(20), nullable=False)
    destino_id = Column(Integer)
    estado = Column(String(20), default="pendiente")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
