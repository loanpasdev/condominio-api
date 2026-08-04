from typing import List
from sqlalchemy.orm import Session
from app.puertos.salida.repositorio_permiso import RepositorioPermiso
from app.infraestructura.modelado.modelo_modulo import ModuloModelo
from app.infraestructura.modelado.modelo_rol_modulo import RolModuloModelo


class RepositorioPermisoSQLAlchemy(RepositorioPermiso):
    def __init__(self, db: Session):
        self.db = db

    def obtener_modulos_por_rol(self, rol: str) -> List[str]:
        resultados = (
            self.db.query(ModuloModelo.codigo)
            .join(RolModuloModelo, RolModuloModelo.modulo_id == ModuloModelo.id)
            .filter(RolModuloModelo.rol == rol)
            .all()
        )
        return [r[0] for r in resultados]

    def obtener_todos_los_modulos(self) -> List[dict]:
        modulos = self.db.query(ModuloModelo).all()
        return [{"id": m.id, "codigo": m.codigo, "nombre": m.nombre} for m in modulos]

    def asignar_modulos_a_rol(self, rol: str, codigos_modulos: List[str]) -> None:
        self.db.query(RolModuloModelo).filter(RolModuloModelo.rol == rol).delete()
        for codigo in codigos_modulos:
            modulo = self.db.query(ModuloModelo).filter(ModuloModelo.codigo == codigo).first()
            if modulo:
                registro = RolModuloModelo(rol=rol, modulo_id=modulo.id)
                self.db.add(registro)
        self.db.commit()
