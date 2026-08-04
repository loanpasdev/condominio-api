from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.tipo_cuenta_bancaria.entidad import TipoCuentaBancaria
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_tipo_cuenta_bancaria import RepositorioTipoCuentaBancaria
from app.infraestructura.modelado.modelo_tipo_cuenta_bancaria import TipoCuentaBancariaModelo


class RepositorioTipoCuentaBancariaSQLAlchemy(RepositorioTipoCuentaBancaria):
    """Implementacion del repositorio de tipos de cuenta bancaria con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[TipoCuentaBancaria]:
        modelo = self.db.query(TipoCuentaBancariaModelo).filter(
            TipoCuentaBancariaModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[TipoCuentaBancaria], int]:
        consulta = self.db.query(TipoCuentaBancariaModelo)

        if buscar:
            consulta = consulta.filter(
                TipoCuentaBancariaModelo.nombre.ilike(f"%{buscar}%")
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, tipo_cuenta: TipoCuentaBancaria) -> TipoCuentaBancaria:
        modelo = TipoCuentaBancariaModelo(
            nombre=tipo_cuenta.nombre,
            condominio_id=tipo_cuenta.condominio_id,
            estado=tipo_cuenta.estado.value,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, tipo_cuenta: TipoCuentaBancaria) -> TipoCuentaBancaria:
        modelo = self.db.query(TipoCuentaBancariaModelo).filter(
            TipoCuentaBancariaModelo.id == tipo_cuenta.id
        ).first()
        if modelo:
            modelo.nombre = tipo_cuenta.nombre
            modelo.condominio_id = tipo_cuenta.condominio_id
            modelo.estado = tipo_cuenta.estado.value
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(TipoCuentaBancariaModelo).filter(
            TipoCuentaBancariaModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: TipoCuentaBancariaModelo) -> TipoCuentaBancaria:
        return TipoCuentaBancaria(
            id=modelo.id,
            nombre=modelo.nombre,
            condominio_id=modelo.condominio_id,
            estado=EstadoUsuario(modelo.estado),
        )

    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        consulta = self.db.query(TipoCuentaBancariaModelo).filter(
            TipoCuentaBancariaModelo.nombre.ilike(nombre),
            TipoCuentaBancariaModelo.condominio_id == condominio_id,
        )
        if excluir_id:
            consulta = consulta.filter(TipoCuentaBancariaModelo.id != excluir_id)
        return consulta.first() is not None
