from dataclasses import dataclass


@dataclass(frozen=True)
class Dinero:
    """Value Object para representar cantidades monetarias"""
    monto: float
    moneda: str = "USD"

    def __post_init__(self):
        if self.monto < 0:
            raise ValueError("El monto no puede ser negativo")

    def sumar(self, otro: "Dinero") -> "Dinero":
        if self.moneda != otro.moneda:
            raise ValueError("No se pueden sumar montos de diferentes monedas")
        return Dinero(monto=self.monto + otro.monto, moneda=self.moneda)

    def restar(self, otro: "Dinero") -> "Dinero":
        if self.moneda != otro.moneda:
            raise ValueError("No se pueden restar montos de diferentes monedas")
        return Dinero(monto=self.monto - otro.monto, moneda=self.moneda)


@dataclass(frozen=True)
class Cedula:
    """Value Object para cedula/RIF"""
    valor: str

    def __post_init__(self):
        if not self.valor or len(self.valor) < 5:
            raise ValueError("La cedula debe tener al menos 5 caracteres")


@dataclass(frozen=True)
class Email:
    """Value Object para email"""
    valor: str

    def __post_init__(self):
        if "@" not in self.valor:
            raise ValueError("Email invalido")


@dataclass(frozen=True)
class Porcentual:
    """Value Object para porcentajes de alicuota"""
    valor: float

    def __post_init__(self):
        if not 0 <= self.valor <= 100:
            raise ValueError("El porcentual debe estar entre 0 y 100")
