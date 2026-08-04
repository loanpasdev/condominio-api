from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.metodo_pago.entidad import MetodoPago
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_metodo_pago import RepositorioMetodoPago
from app.infraestructura.modelado.modelo_metodo_pago import MetodoPagoModelo


class RepositorioMetodoPagoSQLAlchemy(RepositorioMetodoPago):
    """Implementacion del repositorio de metodos de pago con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[MetodoPago]:
        modelo = self.db.query(MetodoPagoModelo).filter(
            MetodoPagoModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[MetodoPago], int]:
        consulta = self.db.query(MetodoPagoModelo)

        if buscar:
            consulta = consulta.filter(
                MetodoPagoModelo.nombre.ilike(f"%{buscar}%")
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, metodo_pago: MetodoPago) -> MetodoPago:
        modelo = MetodoPagoModelo(
            nombre=metodo_pago.nombre,
            condominio_id=metodo_pago.condominio_id,
            estado=metodo_pago.estado.value,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, metodo_pago: MetodoPago) -> MetodoPago:
        modelo = self.db.query(MetodoPagoModelo).filter(
            MetodoPagoModelo.id == metodo_pago.id
        ).first()
        if modelo:
            modelo.nombre = metodo_pago.nombre
            modelo.condominio_id = metodo_pago.condominio_id
            modelo.estado = metodo_pago.estado.value
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(MetodoPagoModelo).filter(
            MetodoPagoModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: MetodoPagoModelo) -> MetodoPago:
        return MetodoPago(
            id=modelo.id,
            nombre=modelo.nombre,
            condominio_id=modelo.condominio_id,
            estado=EstadoUsuario(modelo.estado),
        )

    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        consulta = self.db.query(MetodoPagoModelo).filter(
            MetodoPagoModelo.nombre.ilike(nombre),
            MetodoPagoModelo.condominio_id == condominio_id,
        )
        if excluir_id:
            consulta = consulta.filter(MetodoPagoModelo.id != excluir_id)
        return consulta.first() is not None
