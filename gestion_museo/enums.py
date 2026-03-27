# enums.py
from enum import Enum


class EstadoObra(Enum):
    """Estados posibles de una obra de arte."""

    EXPUESTA = "Expuesta"
    RESTAURACION = "En Restauración"
    CEDIDA = "Cedida"
    DANADA = "Dañada"