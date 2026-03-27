# main.py
# PEP 8: imports agrupados y manejo seguro de ejecución como script/paquete
try:
    from .models import Producto, Catalogo, Tarjeta_Credito
    from .users import Cliente
    from .logistics import Agente_Deposito, Empresa_Transporte
    from .support import Gerente_Relaciones
except ImportError:
    import os
    import sys
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(pkg_dir)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    from tele_ventas.models import Producto, Catalogo, Tarjeta_Credito
    from tele_ventas.users import Cliente
    from tele_ventas.logistics import Agente_Deposito, Empresa_Transporte
    from tele_ventas.support import Gerente_Relaciones

from datetime import datetime


def autenticar_usuario() -> tuple[str, str, str]:
    """Autenticación simplificada por rol con validaciones de credenciales."""
    while True:
        try:
            nombre = input("Nombre del usuario: ").strip()
            correo = input("Correo electrónico: ").strip()
            if not nombre:
                print("Nombre no puede estar vacío.")
                continue
            if not correo:
                print("Correo electrónico no puede estar vacío.")
                continue

            print("\nSeleccione perfil:")
            print("1. Cliente")
            print("2. Agente de Depósito")
            print("3. Gerente de Relaciones")
            perfil = input("Opción de perfil: ").strip()

            if perfil not in {"1", "2", "3"}:
                print("Opción inválida, elija 1, 2 o 3.")
                continue

            if perfil == "3":
                if nombre != "Carlos Mendoza" or correo != "gerente@televentas.com":
                    print("Credenciales de Gerente de Relaciones incorrectas.")
                    continue

            # Roles 1 y 2 aceptan cualquier nombre y correo no vacío.
            return nombre, correo, perfil
        except EOFError:
            print("Ejecución no interactiva detectada. Saliendo.")
            return "", "", "0"


def app() -> None:
    """Punto de entrada principal de la aplicación CLI."""
    catalogo = Catalogo()
    # PEP 8: inicialización controlada con método público
    productos_iniciales = [
        Producto("LAP01", "Laptop Pro", 1200.0, 5),
        Producto("CEL02", "Smartphone X", 800.0, 10),
        Producto("TAB03", "Tablet Z", 450.0, 7),
    ]
    for prod in productos_iniciales:
        catalogo.agregar_producto(prod)

    print("--- BIENVENIDO A TELE-VENTAS ---")

    nombre, correo, rol = autenticar_usuario()
    if rol == "0":
        return

    # Agentes y gerente no requieren dirección.
    cliente = None
    agente = None
    gerente = None
    transportadora = Empresa_Transporte("Logística Express", "555-0199")
    siguiente_id = 1001
    ordenes_global: list = []

    if rol == "1":
        while True:
            try:
                direccion = input("Dirección: ").strip()
                if not direccion:
                    print("Dirección no puede estar vacía.")
                    continue
                break
            except EOFError:
                print("Ejecución no interactiva detectada. Saliendo.")
                return
        cliente = Cliente(nombre, correo, direccion)
        print(f"Acceso concedido Cliente: {nombre} ({correo})")
    elif rol == "2":
        agente = Agente_Deposito("AG-007")
        print(f"Acceso concedido Agente de Depósito: {nombre} ({correo})")
    elif rol == "3":
        gerente = Gerente_Relaciones("GR-1")
        print(f"Acceso concedido Gerente de Relaciones: {nombre} ({correo})")

    if rol != "1":
        # En este taller el comportamiento principal se centra en Cliente.
        print("El usuario autenticado no usa el flujo de cliente en este prototipo. Cerrando aplicación.")
        return

    def mostrar_menu() -> None:
        """Muestra el menú principal (PEP 8: función helper)."""
        print("\nOpciones:")
        print("1. Ver catálogo")
        print("2. Consultar producto por código")
        print("3. Solicitar envío periódico de catálogo por correo")
        print("4. Ingresar nueva orden")
        print("5. Agregar producto a orden existente")
        print("6. Procesar pago de una orden")
        print("7. Cancelar orden")
        print("8. Presentar una queja")
        print("9. Salir")

    while True:
        mostrar_menu()
        try:
            opcion = input("Elija opción: ")
        except EOFError:
            print("Entrada terminada. Saliendo.")
            break

        if opcion == "1":
            for linea in cliente.solicitar_catalogo(catalogo):
                print(linea)
        elif opcion == "2":
            codigo = input("Ingrese código de producto: ")
            print(cliente.solicitar_info_producto(catalogo, codigo))
        elif opcion == "3":
            cliente.solicitar_envio_catalogo()
        elif opcion == "4":
            orden = cliente.ingresar_orden(siguiente_id)
            print(f"Orden creada con id {siguiente_id}")
            siguiente_id += 1
        elif opcion == "5":
            try:
                oid = int(input("Id de orden: "))
            except ValueError:
                print("Entrada inválida, debe ser un número entero.")
                continue
            codigo = input("Código de producto a agregar: ")
            orden = next(
                (o for o in cliente.ordenes if o.id_orden == oid), None
            )
            if orden:
                prod = catalogo.buscar_producto(codigo)
                if prod:
                    orden.agregar_producto(prod)
                    print("Producto añadido.")
                else:
                    print("Producto no encontrado.")
            else:
                print("Orden no existe.")
        elif opcion == "6":
            try:
                oid = int(input("Id de orden a pagar: "))
            except ValueError:
                print("Entrada inválida, debe ser un número entero.")
                continue
            orden = next(
                (o for o in cliente.ordenes if o.id_orden == oid), None
            )
            if orden:
                if orden.estado != "Pendiente":
                    print(f"No se puede pagar, estado actual: {orden.estado}")
                else:
                    num = input("Número de tarjeta: ")
                    venc = input("Fecha de vencimiento (YYYY-MM-DD): ")
                    try:
                        fecha = datetime.fromisoformat(venc)
                    except ValueError:
                        print("Formato de fecha inválido")
                        continue
                    tarjeta = Tarjeta_Credito(num, cliente.nombre, fecha)
                    if orden.procesar_pago(tarjeta):
                        print("Pago procesado con éxito.")
                        agente.armar_pedido(orden)
                        agente.seleccionar_transporte(transportadora, orden)
                    else:
                        print("Fallo el procesamiento del pago.")
            else:
                print("Orden no encontrada.")
        elif opcion == "7":
            try:
                oid = int(input("Id de orden a cancelar: "))
            except ValueError:
                print("Entrada inválida, debe ser un número entero.")
                continue
            if cliente.cancelar_orden(oid):
                print("Orden cancelada.")
            else:
                print("No se pudo cancelar (tal vez no existe o está ya procesada).")
        elif opcion == "8":
            motivo = input("Motivo de la queja: ")
            desc = input("Descripción: ")
            queja = cliente.presentar_queja(motivo, desc)
            queja.enviar_a_gerente(Gerente_Relaciones("GR-1"))
        elif opcion == "9":
            print("Gracias por usar Tele-Ventas. ¡Hasta luego!")
            break
        else:
            print("Opción inválida, inténtelo de nuevo.")


if __name__ == "__main__":
    # PEP 8: configuración de path para ejecución directa
    import os
    import sys
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(pkg_dir)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    app()