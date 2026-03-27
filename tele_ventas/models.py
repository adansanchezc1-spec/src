# models.py
# PEP 8: Imports ordenados (stdlib → third-party → locales)
from typing import List
from datetime import datetime
from .interfaces import MetodoPago


class Producto:
    """Representa un artículo del catálogo.

    Attributes:
        codigo (str): Código único del producto.
        descripcion (str): Nombre/descripción del producto.
        precio (float): Precio unitario en dólares.
        _cantidad_disponible (int): Stock interno (encapsulado).
    """

    def __init__(self, codigo: str, descripcion: str, precio: float, cantidad: int) -> None:
        """Inicializa un nuevo producto."""
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio = precio
        self._cantidad_disponible = cantidad  # atributo privado

    @property
    def cantidad_disponible(self) -> int:
        """Propiedad de solo lectura (encapsulamiento PEP 8)."""
        return self._cantidad_disponible

    def actualizar_disponibilidad(self, cantidad: int) -> None:
        """Actualiza el stock del producto.

        Args:
            cantidad (int): Valor positivo (entrada) o negativo (salida).
        """
        self._cantidad_disponible += cantidad


class Catalogo:
    """Colección de productos con fecha de última actualización."""

    def __init__(self) -> None:
        self._productos: List[Producto] = []  # lista privada
        self.fecha_actualizacion = datetime.now()

    def listar_productos(self) -> List[str]:
        """Devuelve lista de strings con información de cada producto."""
        return [
            f"{p.codigo}: {p.descripcion} (${p.precio})"
            for p in self._productos
        ]

    def buscar_producto(self, codigo: str) -> Producto | None:
        """Busca un producto por código o retorna None."""
        for producto in self._productos:
            if producto.codigo == codigo:
                return producto
        return None

    def agregar_producto(self, producto: Producto) -> None:
        """Método público controlado para agregar productos (encapsulamiento)."""
        self._productos.append(producto)


class Tarjeta_Credito(MetodoPago):
    """Implementación concreta de método de pago con tarjeta."""

    def __init__(
        self, numero: str, titular: str, fecha_vencimiento: datetime
    ) -> None:
        self._numero = numero
        self._titular = titular
        self._fecha_vencimiento = fecha_vencimiento

    @property
    def numero(self) -> str:
        """Número de tarjeta (solo lectura)."""
        return self._numero

    def validar(self) -> bool:
        """Valida que la tarjeta no esté vencida."""
        return self._fecha_vencimiento > datetime.now()

    def procesar(self, monto: float) -> bool:
        """Simula procesamiento de pago."""
        print(f"Procesando pago de ${monto} con tarjeta {self.numero[-4:]}")
        return True


class Orden_Compra:
    """Representa una orden de compra y su ciclo de vida transaccional."""

    def __init__(self, id_orden: int) -> None:
        self.id_orden = id_orden
        self._estado = "Pendiente"  # atributo privado
        self.fecha_creacion = datetime.now()
        self._productos: List[Producto] = []

    @property
    def estado(self) -> str:
        """Estado actual de la orden (solo lectura)."""
        return self._estado

    def _validar_transicion(self, nuevo_estado: str) -> bool:
        """Método privado: lógica interna de transiciones de estado."""
        # Aquí se podrían añadir reglas de negocio complejas
        return True

    def actualizar_estado(self, nuevo_estado: str) -> None:
        """Método público controlado para cambiar estado (encapsulamiento)."""
        if self._validar_transicion(nuevo_estado):
            self._estado = nuevo_estado

    def __str__(self) -> str:
        prods = ", ".join(p.codigo for p in self._productos)
        return f"Orden {self.id_orden} [{self.estado}] productos: {prods}"

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega un producto a la orden y reduce stock."""
        if producto.cantidad_disponible > 0:
            self._productos.append(producto)
            producto.actualizar_disponibilidad(-1)

    def calcular_total(self) -> float:
        """Calcula el monto total de la orden."""
        return sum(p.precio for p in self._productos)

    def procesar_pago(self, metodo: MetodoPago) -> bool:
        """Procesa el pago y actualiza estado si es exitoso."""
        if metodo.validar():
            total = self.calcular_total()
            if metodo.procesar(total):
                self.actualizar_estado("Confirmada")
                return True
        return False

    def cancelar(self) -> bool:
        """Cancela la orden si aún es posible."""
        if self.estado in ("Pendiente", "Confirmada"):
            self.actualizar_estado("Cancelada")
            return True
        return False