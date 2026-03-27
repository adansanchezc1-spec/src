# users.py
from typing import List
from .models import Orden_Compra, Catalogo
from .support import Queja


class Cliente:
    """Actor principal del sistema de televentas."""

    def __init__(self, nombre: str, correo_electronico: str, direccion: str) -> None:
        self.nombre = nombre
        self.correo_electronico = correo_electronico
        self.direccion = direccion
        self._ordenes: list[Orden_Compra] = []
        self._catalogo_periodico = False

    @property
    def ordenes(self) -> list[Orden_Compra]:
        """Devuelve copia segura de las órdenes (encapsulamiento)."""
        return self._ordenes[:]

    def solicitar_catalogo(self, catalogo: Catalogo) -> List[str]:
        """Solicita listado completo del catálogo."""
        return catalogo.listar_productos()

    def solicitar_info_producto(self, catalogo: Catalogo, codigo: str) -> str:
        """Solicita información detallada de un producto."""
        prod = catalogo.buscar_producto(codigo)
        if prod:
            return (
                f"{prod.codigo} - {prod.descripcion}: ${prod.precio}, "
                f"disponibles {prod.cantidad_disponible}"
            )
        return "Producto no encontrado."

    def solicitar_envio_catalogo(self) -> None:
        """Activa envío periódico de catálogo por correo."""
        self._catalogo_periodico = True
        print(
            f"{self.nombre} recibirá próximamente el catálogo en "
            f"{self.correo_electronico}"
        )

    def ingresar_orden(self, id_orden: int) -> Orden_Compra:
        """Crea y registra una nueva orden."""
        orden = Orden_Compra(id_orden)
        self._ordenes.append(orden)
        return orden

    def cancelar_orden(self, id_orden: int) -> bool:
        """Cancela una orden por su ID."""
        for orden in self._ordenes:
            if orden.id_orden == id_orden:
                return orden.cancelar()
        return False

    def presentar_queja(self, motivo: str, desc: str) -> Queja:
        """Crea y devuelve una nueva queja."""
        return Queja(motivo, desc)