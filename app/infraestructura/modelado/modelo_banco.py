from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime


class BancoModelo(Base):
    __tablename__ = "bancos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
