from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Time
from app.database import Base
from datetime import datetime


class ReservaModelo(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=True)
    area_comun_id = Column(Integer, ForeignKey("areas_comunes.id"), nullable=True)
    propietario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    estado = Column(String(20), default="confirmada")
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
