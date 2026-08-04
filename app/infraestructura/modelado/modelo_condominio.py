from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base
from datetime import datetime


class CondominioModelo(Base):
    __tablename__ = "condominios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    rif = Column(String(20), unique=True, nullable=False)
    direccion = Column(Text, nullable=False)
    telefono = Column(String(20))
    email = Column(String(100))
    logo = Column(Text)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
