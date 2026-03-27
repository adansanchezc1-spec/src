# interfaces.py
from abc import ABC, abstractmethod


class MetodoPago(ABC):
    """Interfaz abstracta para cualquier método de pago.

    Implementaciones deben proporcionar validar() y procesar().
    """

    @abstractmethod
    def validar(self) -> bool:
        """Valida que el método de pago sea usable."""

    @abstractmethod
    def procesar(self, monto: float) -> bool:
        """Ejecuta el cobro del monto indicado."""