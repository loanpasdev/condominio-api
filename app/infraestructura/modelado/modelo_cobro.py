from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Text, Date
from app.database import Base
from datetime import datetime


class CobroModelo(Base):
    __tablename__ = "cobros"

    id = Column(Integer, primary_key=True, index=True)
    condominio_id = Column(Integer, ForeignKey("condominios.id"), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias_gasto.id"), nullable=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    descripcion = Column(Text, nullable=False)
    monto = Column(Numeric(10, 2), nullable=False)
    fecha = Column(Date, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
