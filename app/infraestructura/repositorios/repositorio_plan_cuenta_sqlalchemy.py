from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.plan_cuenta.entidad import PlanCuenta
from app.puertos.salida.repositorio_plan_cuenta import RepositorioPlanCuenta
from app.infraestructura.modelado.modelo_plan_cuenta import PlanCuentaModelo


class RepositorioPlanCuentaSQLAlchemy(RepositorioPlanCuenta):
    """Implementacion del repositorio de plan de cuentas con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[PlanCuenta]:
        modelo = self.db.query(PlanCuentaModelo).filter(
            PlanCuentaModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[PlanCuenta], int]:
        consulta = self.db.query(PlanCuentaModelo)

        if buscar:
            consulta = consulta.filter(
                or_(
                    PlanCuentaModelo.nombre.ilike(f"%{buscar}%"),
                    PlanCuentaModelo.codigo.ilike(f"%{buscar}%"),
                )
            )

        total = consulta.count()
        modelos = consulta.order_by(PlanCuentaModelo.codigo).offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, cuenta: PlanCuenta) -> PlanCuenta:
        modelo = PlanCuentaModelo(
            codigo=cuenta.codigo,
            nombre=cuenta.nombre,
            tipo=cuenta.tipo,
            descripcion=cuenta.descripcion,
            padre_id=cuenta.padre_id,
            activo=cuenta.activo,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, cuenta: PlanCuenta) -> PlanCuenta:
        modelo = self.db.query(PlanCuentaModelo).filter(
            PlanCuentaModelo.id == cuenta.id
        ).first()
        if modelo:
            modelo.codigo = cuenta.codigo
            modelo.nombre = cuenta.nombre
            modelo.tipo = cuenta.tipo
            modelo.descripcion = cuenta.descripcion
            modelo.padre_id = cuenta.padre_id
            modelo.activo = cuenta.activo
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(PlanCuentaModelo).filter(
            PlanCuentaModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: PlanCuentaModelo) -> PlanCuenta:
        return PlanCuenta(
            id=modelo.id,
            codigo=modelo.codigo,
            nombre=modelo.nombre,
            tipo=modelo.tipo,
            descripcion=modelo.descripcion,
            padre_id=modelo.padre_id,
            activo=modelo.activo,
        )
