from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.moneda.entidad import Moneda
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_moneda import RepositorioMoneda
from app.infraestructura.modelado.modelo_moneda import MonedaModelo


class RepositorioMonedaSQLAlchemy(RepositorioMoneda):
    """Implementacion del repositorio de monedas con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Moneda]:
        modelo = self.db.query(MonedaModelo).filter(
            MonedaModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Moneda], int]:
        consulta = self.db.query(MonedaModelo)

        if buscar:
            consulta = consulta.filter(
                or_(
                    MonedaModelo.nombre.ilike(f"%{buscar}%"),
                    MonedaModelo.codigo.ilike(f"%{buscar}%"),
                )
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, moneda: Moneda) -> Moneda:
        modelo = MonedaModelo(
            codigo=moneda.codigo,
            nombre=moneda.nombre,
            simbolo=moneda.simbolo,
            estado=moneda.estado.value,
            es_base=moneda.es_base,
            tasa_cambio=moneda.tasa_cambio,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, moneda: Moneda) -> Moneda:
        modelo = self.db.query(MonedaModelo).filter(
            MonedaModelo.id == moneda.id
        ).first()
        if modelo:
            modelo.codigo = moneda.codigo
            modelo.nombre = moneda.nombre
            modelo.simbolo = moneda.simbolo
            modelo.estado = moneda.estado.value
            modelo.es_base = moneda.es_base
            modelo.tasa_cambio = moneda.tasa_cambio
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(MonedaModelo).filter(
            MonedaModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def existe_nombre(self, nombre: str, excluir_id: int = None) -> bool:
        consulta = self.db.query(MonedaModelo).filter(MonedaModelo.nombre.ilike(nombre))
        if excluir_id:
            consulta = consulta.filter(MonedaModelo.id != excluir_id)
        return consulta.first() is not None

    def _mapear_a_entidad(self, modelo: MonedaModelo) -> Moneda:
        return Moneda(
            id=modelo.id,
            codigo=modelo.codigo,
            nombre=modelo.nombre,
            simbolo=modelo.simbolo,
            estado=EstadoUsuario(modelo.estado),
            es_base=bool(modelo.es_base),
            tasa_cambio=float(modelo.tasa_cambio) if modelo.tasa_cambio else 1.0,
        )
