from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text
from app.database import Base
from datetime import datetime


class PagoModelo(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=True)
    cuota_id = Column(Integer, ForeignKey("cuotas.id"), nullable=True)
    propietario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    monto = Column(Numeric(10, 2), nullable=False)
    metodo_pago_id = Column(Integer, ForeignKey("metodos_pago.id"), nullable=True)
    moneda_id = Column(Integer, ForeignKey("monedas.id"), nullable=True)
    referencia = Column(String(100))
    fecha_pago = Column(DateTime, nullable=False)
    notas = Column(Text)
    estado = Column(String(20), default="completado")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
