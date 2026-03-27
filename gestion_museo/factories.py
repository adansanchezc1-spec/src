# factories.py
# PEP 8: Patrón Factory Method
from inventory import Cuadro, Escultura, Otro_Objeto


class ObraFactory:
    """Fábrica que desacopla la creación de obras."""

    @staticmethod
    def crear_obra(tipo: str, **kwargs) -> "Obra_Arte":
        """Crea la instancia correcta según el tipo."""
        tipo = tipo.lower()
        if tipo == "cuadro":
            return Cuadro(**kwargs)
        if tipo == "escultura":
            return Escultura(**kwargs)
        if tipo == "otro":
            return Otro_Objeto(**kwargs)
        raise ValueError("Tipo de obra inválido")
        