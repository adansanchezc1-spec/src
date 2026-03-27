# operations.py
from datetime import date, timedelta


class Restauracion:
    """Registro de un proceso de restauración."""

    def __init__(self, tipo: str, fecha_inicio: date, causa: str = "Mantenimiento Preventivo") -> None:
        self._tipo = tipo
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = None
        self._causa = causa

    @property
    def tipo(self) -> str:
        """Tipo de restauración (solo lectura)."""
        return self._tipo

    @property
    def fecha_inicio(self) -> date:
        """Fecha de inicio (solo lectura)."""
        return self._fecha_inicio

    @property
    def fecha_fin(self) -> date | None:
        """Fecha de fin (solo lectura)."""
        return self._fecha_fin

    @property
    def causa(self) -> str:
        """Causa de la restauración (solo lectura)."""
        return self._causa

    def finalizar(self, fecha_fin: date) -> None:
        """Finaliza el proceso de restauración."""
        self._fecha_fin = fecha_fin

    def antiguedad_dias(self, fecha_actual: date) -> int:
        """Devuelve antigüedad desde el inicio de la restauración."""
        return (fecha_actual - self._fecha_inicio).days


class Museo_Colaborador:
    """Institución externa receptora de cesiones."""

    def __init__(self, nombre: str, ciudad: str) -> None:
        self._nombre = nombre
        self._ciudad = ciudad

    @property
    def nombre(self) -> str:
        """Nombre del museo colaborador (solo lectura)."""
        return self._nombre

    @property
    def ciudad(self) -> str:
        """Ciudad del museo colaborador (solo lectura)."""
        return self._ciudad


class Cesion:
    """Registro de préstamo temporal a otro museo."""

    def __init__(self, museo: Museo_Colaborador, importe: float, periodo_dias: int, fecha_inicio: date) -> None:
        self._museo = museo
        self._importe = importe
        self._periodo_dias = periodo_dias
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = None

    @property
    def museo(self) -> Museo_Colaborador:
        """Museo colaborador (solo lectura)."""
        return self._museo

    @property
    def importe(self) -> float:
        """Importe de la cesión (solo lectura)."""
        return self._importe

    @property
    def periodo_dias(self) -> int:
        """Período en días (solo lectura)."""
        return self._periodo_dias

    @property
    def fecha_inicio(self) -> date:
        """Fecha de inicio (solo lectura)."""
        return self._fecha_inicio

    @property
    def fecha_fin(self) -> date | None:
        """Fecha de fin (solo lectura)."""
        return self._fecha_fin

    def finalizar(self, fecha_fin: date) -> None:
        """Termina la cesión."""
        self._fecha_fin = fecha_fin

    def esta_vigente(self, fecha_actual: date) -> bool:
        """Indica si la cesión está vigente en la fecha actual."""
        expiration = self._fecha_inicio + timedelta(days=self._periodo_dias)
        if self._fecha_fin is not None:
            return self._fecha_inicio <= fecha_actual < self._fecha_fin
        return self._fecha_inicio <= fecha_actual < expiration