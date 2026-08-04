from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from app.database import Base
from datetime import datetime


class CuentaBancariaModelo(Base):
    __tablename__ = "cuentas_bancarias"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=True)
    banco_id = Column(Integer, ForeignKey("bancos.id"), nullable=True)
    tipo_cuenta_id = Column(Integer, ForeignKey("tipos_cuenta_bancaria.id"), nullable=True)
    numero_cuenta = Column(String(30), nullable=False)
    titular = Column(String(100), nullable=False)
    moneda_id = Column(Integer, ForeignKey("monedas.id"), nullable=True)
    saldo = Column(Numeric(12, 2), default=0)
    estado = Column(String(20), default="activo")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
