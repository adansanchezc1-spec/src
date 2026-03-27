# logistics.py
from .models import Orden_Compra


class Agente_Deposito:
    """Responsable de preparar y asignar pedidos."""

    def __init__(self, identificacion: str) -> None:
        self.identificacion = identificacion

    def consultar_ordenes(self, ordenes: list[Orden_Compra]) -> list[Orden_Compra]:
        """Filtra órdenes en estado Confirmada."""
        return [o for o in ordenes if o.estado == "Confirmada"]

    def armar_pedido(self, orden: Orden_Compra) -> None:
        """Arma el paquete y actualiza estado."""
        print(f"Agente {self.identificacion} armando paquete para Orden {orden.id_orden}")
        orden.actualizar_estado("Empaquetado")

    def seleccionar_transporte(
        self, transporte: "Empresa_Transporte", orden: Orden_Compra
    ) -> None:
        """Asigna transportista y delega entrega."""
        print(f"Asignando orden {orden.id_orden} a {transporte.nombre}")
        transporte.entregar_pedido(orden)


class Empresa_Transporte:
    """Empresa externa que realiza la entrega física."""

    def __init__(self, nombre: str, telefono: str) -> None:
        self.nombre = nombre
        self.telefono = telefono

    def entregar_pedido(self, orden: Orden_Compra) -> None:
        """Marca la orden como entregada."""
        print(f"[{self.nombre}] Entregando orden {orden.id_orden}...")
        orden.actualizar_estado("Entregado")