from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from app.database import Base
from datetime import datetime


class PlanCuentaModelo(Base):
    __tablename__ = "plan_cuentas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    # Valores: 'activo', 'pasivo', 'patrimonio', 'ingreso', 'gasto'
    tipo = Column(String(20), nullable=False)
    descripcion = Column(Text)
    padre_id = Column(Integer)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
