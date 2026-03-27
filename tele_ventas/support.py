# support.py
from datetime import datetime


class Gerente_Relaciones:
    """Gestor de atención al cliente."""

    def __init__(self, identificacion: str) -> None:
        self.identificacion = identificacion

    def recibir_queja(self, queja: "Queja") -> None:
        """Registra recepción de queja."""
        print(f"Gerente {self.identificacion} recibió queja: {queja.motivo}")

    def gestionar_queja(self, queja: "Queja") -> None:
        """Inicia proceso de resolución."""
        print(f"Resolviendo queja {queja.motivo}...")


class Queja:
    """Registro de reclamación de cliente."""

    def __init__(self, motivo: str, descripcion: str) -> None:
        self._motivo = motivo
        self._descripcion_detallada = descripcion
        self._fecha = datetime.now()

    @property
    def motivo(self) -> str:
        """Motivo de la queja (solo lectura)."""
        return self._motivo

    @property
    def descripcion_detallada(self) -> str:
        """Descripción completa (solo lectura)."""
        return self._descripcion_detallada

    def enviar_a_gerente(self, gerente: Gerente_Relaciones) -> None:
        """Envía la queja al gerente correspondiente."""
        gerente.recibir_queja(self)