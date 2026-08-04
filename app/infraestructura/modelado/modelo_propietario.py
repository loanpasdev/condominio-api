from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from app.database import Base
from datetime import datetime


class PropietarioModelo(Base):
    __tablename__ = "propietarios"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cedula = Column(String(20), nullable=False)
    correo = Column(String(100), nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
