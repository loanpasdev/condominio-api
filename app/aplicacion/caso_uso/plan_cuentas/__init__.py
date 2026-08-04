from app.dominio.plan_cuenta.entidad import PlanCuenta
from app.dominio.plan_cuenta.excepciones import PlanCuentaNoExiste
from app.puertos.salida.repositorio_plan_cuenta import RepositorioPlanCuenta


class CrearPlanCuenta:
    def __init__(self, repositorio: RepositorioPlanCuenta):
        self.repositorio = repositorio

    def ejecutar(self, codigo: str, nombre: str, tipo: str, descripcion: str = None, padre_id: int = None) -> PlanCuenta:
        cuenta = PlanCuenta(
            codigo=codigo, nombre=nombre, tipo=tipo,
            descripcion=descripcion, padre_id=padre_id,
        )
        return self.repositorio.crear(cuenta)


class ListarPlanCuentas:
    def __init__(self, repositorio: RepositorioPlanCuenta):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, pagina=pagina, por_pagina=por_pagina)


class ObtenerPlanCuenta:
    def __init__(self, repositorio: RepositorioPlanCuenta):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> PlanCuenta:
        cuenta = self.repositorio.obtener_por_id(id)
        if not cuenta:
            raise PlanCuentaNoExiste("Cuenta no encontrada")
        return cuenta


class ActualizarPlanCuenta:
    def __init__(self, repositorio: RepositorioPlanCuenta):
        self.repositorio = repositorio

    def ejecutar(self, id: int, codigo: str, nombre: str, tipo: str, descripcion: str, padre_id: int, activo: bool) -> PlanCuenta:
        cuenta = self.repositorio.obtener_por_id(id)
        if not cuenta:
            raise PlanCuentaNoExiste("Cuenta no encontrada")

        cuenta.codigo = codigo
        cuenta.nombre = nombre
        cuenta.tipo = tipo
        cuenta.descripcion = descripcion
        cuenta.padre_id = padre_id
        cuenta.activo = activo
        return self.repositorio.actualizar(cuenta)


class EliminarPlanCuenta:
    def __init__(self, repositorio: RepositorioPlanCuenta):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        cuenta = self.repositorio.obtener_por_id(id)
        if not cuenta:
            raise PlanCuentaNoExiste("Cuenta no encontrada")
        return self.repositorio.eliminar(id)
