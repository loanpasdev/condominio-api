from app.dominio.cuenta_bancaria.entidad import CuentaBancaria
from app.dominio.cuenta_bancaria.excepciones import CuentaBancariaNoExiste
from app.puertos.salida.repositorio_cuenta_bancaria import RepositorioCuentaBancaria
from app.puertos.salida.repositorio_condominio import RepositorioCondominio
from app.dominio.condominio.excepciones import CondominioNoExiste


class CrearCuentaBancaria:
    def __init__(self, repositorio: RepositorioCuentaBancaria, repositorio_condominio: RepositorioCondominio):
        self.repositorio = repositorio
        self.repositorio_condominio = repositorio_condominio

    def ejecutar(self, condominio_id: int = None, banco_id: int = None, tipo_cuenta_id: int = None, numero_cuenta: str = '', titular: str = '', moneda_id: int = None, saldo: float = 0) -> CuentaBancaria:
        return self.repositorio.crear(CuentaBancaria(
            condominio_id=condominio_id or 1, banco_id=banco_id,
            tipo_cuenta_id=tipo_cuenta_id, numero_cuenta=numero_cuenta,
            titular=titular, moneda_id=moneda_id, saldo=saldo,
        ))


class ListarCuentasBancarias:
    def __init__(self, repositorio: RepositorioCuentaBancaria):
        self.repositorio = repositorio

    def ejecutar(self, buscar: str = None, condominio_id: int = None, pagina: int = 1, por_pagina: int = 10) -> tuple:
        return self.repositorio.listar(buscar=buscar, condominio_id=condominio_id, pagina=pagina, por_pagina=por_pagina)


class ObtenerCuentaBancaria:
    def __init__(self, repositorio: RepositorioCuentaBancaria):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> CuentaBancaria:
        cuenta = self.repositorio.obtener_por_id(id)
        if not cuenta:
            raise CuentaBancariaNoExiste("Cuenta bancaria no encontrada")
        return cuenta


class ActualizarCuentaBancaria:
    def __init__(self, repositorio: RepositorioCuentaBancaria):
        self.repositorio = repositorio

    def ejecutar(self, id: int, banco_id: int = None, tipo_cuenta_id: int = None, numero_cuenta: str = None, titular: str = None, moneda_id: int = None, saldo: float = None, estado: str = None) -> CuentaBancaria:
        cuenta = self.repositorio.obtener_por_id(id)
        if not cuenta:
            raise CuentaBancariaNoExiste("Cuenta bancaria no encontrada")
        if banco_id is not None: cuenta.banco_id = banco_id
        if tipo_cuenta_id is not None: cuenta.tipo_cuenta_id = tipo_cuenta_id
        if numero_cuenta is not None: cuenta.numero_cuenta = numero_cuenta
        if titular is not None: cuenta.titular = titular
        if moneda_id is not None: cuenta.moneda_id = moneda_id
        if saldo is not None: cuenta.saldo = saldo
        if estado is not None: cuenta.estado = estado
        return self.repositorio.actualizar(cuenta)


class EliminarCuentaBancaria:
    def __init__(self, repositorio: RepositorioCuentaBancaria):
        self.repositorio = repositorio

    def ejecutar(self, id: int) -> bool:
        cuenta = self.repositorio.obtener_por_id(id)
        if not cuenta:
            raise CuentaBancariaNoExiste("Cuenta bancaria no encontrada")
        return self.repositorio.eliminar(id)
