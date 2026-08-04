from typing import Optional, List
from sqlalchemy.orm import Session
from app.dominio.area_comun.entidad import AreaComun
from app.dominio.usuario.valores import EstadoUsuario
from app.puertos.salida.repositorio_area_comun import RepositorioAreaComun
from app.infraestructura.modelado.modelo_area_comun import AreaComunModelo


class RepositorioAreaComunSQLAlchemy(RepositorioAreaComun):
    """Implementacion del repositorio de areas comunes con SQLAlchemy"""

    def __init__(self, db: Session):
        self.db = db

    def obtener_por_id(self, id: int) -> Optional[AreaComun]:
        modelo = self.db.query(AreaComunModelo).filter(
            AreaComunModelo.id == id
        ).first()
        if not modelo:
            return None
        return self._mapear_a_entidad(modelo)

    def listar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple[List[AreaComun], int]:
        consulta = self.db.query(AreaComunModelo)

        if buscar:
            consulta = consulta.filter(
                AreaComunModelo.nombre.ilike(f"%{buscar}%")
            )

        total = consulta.count()
        modelos = consulta.offset((pagina - 1) * por_pagina).limit(por_pagina).all()
        return [self._mapear_a_entidad(m) for m in modelos], total

    def crear(self, area: AreaComun) -> AreaComun:
        modelo = AreaComunModelo(
            nombre=area.nombre,
            condominio_id=area.condominio_id,
            descripcion=area.descripcion,
            capacidad=area.capacidad,
            tarifa=area.tarifa,
            hora_inicio=area.hora_inicio,
            hora_fin=area.hora_fin,
            estado=area.estado.value,
        )
        self.db.add(modelo)
        self.db.commit()
        self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def actualizar(self, area: AreaComun) -> AreaComun:
        modelo = self.db.query(AreaComunModelo).filter(
            AreaComunModelo.id == area.id
        ).first()
        if modelo:
            modelo.nombre = area.nombre
            modelo.condominio_id = area.condominio_id
            modelo.descripcion = area.descripcion
            modelo.capacidad = area.capacidad
            modelo.tarifa = area.tarifa
            modelo.hora_inicio = area.hora_inicio
            modelo.hora_fin = area.hora_fin
            modelo.estado = area.estado.value
            self.db.commit()
            self.db.refresh(modelo)
        return self._mapear_a_entidad(modelo)

    def eliminar(self, id: int) -> bool:
        modelo = self.db.query(AreaComunModelo).filter(
            AreaComunModelo.id == id
        ).first()
        if not modelo:
            return False
        self.db.delete(modelo)
        self.db.commit()
        return True

    def _mapear_a_entidad(self, modelo: AreaComunModelo) -> AreaComun:
        return AreaComun(
            id=modelo.id,
            nombre=modelo.nombre,
            condominio_id=modelo.condominio_id,
            descripcion=modelo.descripcion,
            capacidad=modelo.capacidad,
            tarifa=float(modelo.tarifa) if modelo.tarifa else 0,
            hora_inicio=str(modelo.hora_inicio) if modelo.hora_inicio else None,
            hora_fin=str(modelo.hora_fin) if modelo.hora_fin else None,
            estado=EstadoUsuario(modelo.estado),
        )

    def existe_nombre_en_condominio(self, nombre: str, condominio_id: int, excluir_id: int = None) -> bool:
        consulta = self.db.query(AreaComunModelo).filter(
            AreaComunModelo.nombre.ilike(nombre),
            AreaComunModelo.condominio_id == condominio_id,
        )
        if excluir_id:
            consulta = consulta.filter(AreaComunModelo.id != excluir_id)
        return consulta.first() is not None
