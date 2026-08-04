from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, UniqueConstraint
from app.database import Base
from datetime import datetime


class CuotaModelo(Base):
    __tablename__ = "cuotas"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=True)
    unidad_id = Column(Integer, ForeignKey("unidades.id"), nullable=True)
    mes = Column(Integer, nullable=False)
    anio = Column(Integer, nullable=False)
    monto_total = Column(Numeric(10, 2), nullable=False)
    estado = Column(String(20), default="pendiente")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (UniqueConstraint("unidad_id", "mes", "anio", name="uq_cuota_unidad_periodo"),)
