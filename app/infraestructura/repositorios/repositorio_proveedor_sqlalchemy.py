from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.dominio.proveedor.entidad import Proveedor
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_proveedor import RepositorioProveedor
from app.infraestructura.modelado.modelo_proveedor import ProveedorModelo


class RepositorioProveedorSQLAlchemy(RepositorioProveedor):
    """Implementacion del repositorio de proveedores con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[Proveedor]:
        modelo = self.db.query(ProveedorModelo).filter(
            ProveedorModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[Proveedor], int]:
        consulta = self.db.query(ProveedorModelo)

        if buscar:
            consulta = consulta.filter(
                or_(
                    ProveedorModelo.nombre.ilike(f"%{buscar}%"),
                    ProveedorModelo.rif.ilike(f"%{buscar}%"),
                )
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, proveedor: Proveedor) -> Proveedor:
        modelo = ProveedorModelo(
            nombre=proveedor.nombre,
            rif=proveedor.rif,
            condominio_id=proveedor.condominio_id,
            telefono=proveedor.telefono,
            email=proveedor.email,
            estado=proveedor.estado.value,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, proveedor: Proveedor) -> Proveedor:
        modelo = self.db.query(ProveedorModelo).filter(
            ProveedorModelo.id == proveedor.id
        ).first()
        if modelo:
            modelo.nombre = proveedor.nombre
            modelo.rif = proveedor.rif
            modelo.condominio_id = proveedor.condominio_id
            modelo.telefono = proveedor.telefono
            modelo.email = proveedor.email
            modelo.estado = proveedor.estado.value
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(ProveedorModelo).filter(
            ProveedorModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: ProveedorModelo) -> Proveedor:
        return Proveedor(
            id=modelo.id,
            nombre=modelo.nombre,
            rif=modelo.rif,
            condominio_id=modelo.condominio_id,
            telefono=modelo.telefono,
            email=modelo.email,
            estado=EstadoUsuario(modelo.estado),
        )

    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        consulta = self.db.query(ProveedorModelo).filter(
            ProveedorModelo.nombre.ilike(nombre),
            ProveedorModelo.condominio_id == condominio_id,
        )
        if excluir_id:
            consulta = consulta.filter(ProveedorModelo.id != excluir_id)
        return consulta.first() is not None
