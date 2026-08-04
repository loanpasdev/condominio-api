from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Boolean
from app.database import Base
from datetime import datetime


class UnidadModelo(Base):
    __tablename__ = "unidades"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=False)
    tipo_unidad_id = Column(Integer, ForeignKey("tipos_unidad.id"), nullable=False)
    propietario_id = Column(Integer, ForeignKey("propietarios.id"), nullable=True)
    numero = Column(String(10), nullable=False)
    piso = Column(String(20))
    metraje = Column(Numeric(8, 2), nullable=False)
    porcentual = Column(Numeric(5, 2), nullable=False)
    grupo_residencial_id = Column(Integer, ForeignKey("grupos_residenciales.id"), nullable=True)
    habitaciones = Column(Integer, default=0)
    banios = Column(Integer, default=0)
    terraza = Column(Boolean, default=False)
    balcon = Column(Boolean, default=False)
    parking = Column(Boolean, default=False)
    notas = Column(String(500))
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
