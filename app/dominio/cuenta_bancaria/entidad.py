from app.dominio.entidad_base import Entidad


class CuentaBancaria(Entidad):
    def __init__(
        self,
        condominio_id: int,
        banco_id: int,
        tipo_cuenta_id: int,
        numero_cuenta: str,
        titular: str,
        moneda_id: int,
        saldo: float = 0,
        estado: str = "activo",
        id: int = None,
    ):
        super().__init__(id)
        self.condominio_id = condominio_id
        self.banco_id = banco_id
        self.tipo_cuenta_id = tipo_cuenta_id
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.moneda_id = moneda_id
        self.saldo = saldo
        self.estado = estado
