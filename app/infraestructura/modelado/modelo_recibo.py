from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from app.database import Base
from datetime import datetime


class ReciboModelo(Base):
    __tablename__ = "recibos"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id"), nullable=True)
    propietario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    subtotal = Column(Numeric(10, 2), nullable=False)
    mora = Column(Numeric(10, 2), default=0)
    total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(20), default="pendiente")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
