from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.cuenta_bancaria.entidad import CuentaBancaria
from app.puertos.salida.repositorio_cuenta_bancaria import RepositorioCuentaBancaria
from app.infraestructura.modelado.modelo_cuenta_bancaria import CuentaBancariaModelo


class RepositorioCuentaBancariaSQLAlchemy(RepositorioCuentaBancaria):
    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[CuentaBancaria]:
        modelo = self.db.query(CuentaBancariaModelo).filter(CuentaBancariaModelo.id == id).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[CuentaBancaria], int]:
        consulta = self.db.query(CuentaBancariaModelo)
        if buscar:
            consulta = consulta.filter(CuentaBancariaModelo.numero_cuenta.ilike(f"%{buscar}%"))
        if condominio_id:
            consulta = consulta.filter(CuentaBancariaModelo.condominio_id == condominio_id)
        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, cuenta: CuentaBancaria) -> CuentaBancaria:
        modelo = CuentaBancariaModelo(
            condominio_id=cuenta.condominio_id, banco_id=cuenta.banco_id,
            tipo_cuenta_id=cuenta.tipo_cuenta_id, numero_cuenta=cuenta.numero_cuenta,
            titular=cuenta.titular, moneda_id=cuenta.moneda_id,
            saldo=cuenta.saldo, estado=cuenta.estado,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, cuenta: CuentaBancaria) -> CuentaBancaria:
        modelo = self.db.query(CuentaBancariaModelo).filter(CuentaBancariaModelo.id == cuenta.id).first()
        if modelo:
            modelo.banco_id = cuenta.banco_id
            modelo.tipo_cuenta_id = cuenta.tipo_cuenta_id
            modelo.numero_cuenta = cuenta.numero_cuenta
            modelo.titular = cuenta.titular
            modelo.moneda_id = cuenta.moneda_id
            modelo.saldo = cuenta.saldo
            modelo.estado = cuenta.estado
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(CuentaBancariaModelo).filter(CuentaBancariaModelo.id == id).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: CuentaBancariaModelo) -> CuentaBancaria:
        return CuentaBancaria(
            id=modelo.id, condominio_id=modelo.condominio_id,
            banco_id=modelo.banco_id, tipo_cuenta_id=modelo.tipo_cuenta_id,
            numero_cuenta=modelo.numero_cuenta, titular=modelo.titular,
            moneda_id=modelo.moneda_id, saldo=float(modelo.saldo),
            estado=modelo.estado,
        )
