# main.py
# PEP 8: imports agrupados y manejo seguro de ejecución como script/paquete
try:
    from .models import Producto, Catalogo, Tarjeta_Credito
    from .users import Cliente
    from .logistics import Agente_Deposito, Empresa_Transporte
    from .support import Gerente_Relaciones, Queja
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
    from tele_ventas.support import Gerente_Relaciones, Queja

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
            print("0. Salir")
            print("1. Cliente")
            print("2. Agente de Depósito")
            print("3. Gerente de Relaciones")
            perfil = input("Opción de perfil: ").strip()

            if perfil == "0":
                return "", "", "0"

            if perfil not in {"1", "2", "3"}:
                print("Opción inválida, elija 0, 1, 2 o 3.")
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

    transportadora = Empresa_Transporte("Logística Express", "555-0199")
    siguiente_id = 1001
    ordenes_global: list = []
    lista_quejas: list[Queja] = []
    gerente = Gerente_Relaciones("GR-1")

    while True:
        nombre, correo, rol = autenticar_usuario()
        if rol == "0":
            print("Saliendo de la aplicación.")
            break

        # Agentes no requieren dirección.
        cliente = None
        agente = None

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
            agente = Agente_Deposito("AG-007")
            print(f"Acceso concedido Cliente: {nombre} ({correo})")
        elif rol == "2":
            agente = Agente_Deposito("AG-007")
            print(f"Acceso concedido Agente de Depósito: {nombre} ({correo})")

            while True:
                print("\nMenú Agente de Depósito:")
                print("1. Ver órdenes pagadas")
                print("2. Confirmar orden")
                print("3. Armar pedido")
                print("4. Asignar transporte a orden")
                print("5. Cerrar sesión de agente")
                opcion_agente = input("Elija opción: ").strip()

                if opcion_agente == "1":
                    ordenes = agente.consultar_ordenes(ordenes_global)
                    if not ordenes:
                        print("No hay órdenes pagadas en este momento.")
                    else:
                        for o in ordenes:
                            print(o)

                elif opcion_agente == "2":
                    ordenes = agente.consultar_ordenes(ordenes_global)
                    if not ordenes:
                        print("No hay órdenes pagadas para confirmar.")
                        continue
                    try:
                        oid = int(input("Ingrese ID de orden a confirmar: "))
                    except ValueError:
                        print("ID inválido.")
                        continue
                    orden = next((o for o in ordenes if o.id_orden == oid), None)
                    if not orden:
                        print("Orden no encontrada o no está pagada.")
                        continue
                    orden.actualizar_estado("Confirmada")
                    print(f"Orden {oid} confirmada.")

                elif opcion_agente == "3":
                    ordenes_confirmadas = [o for o in ordenes_global if o.estado == "Confirmada"]
                    if not ordenes_confirmadas:
                        print("No hay órdenes confirmadas para armar.")
                        continue
                    try:
                        oid = int(input("Ingrese ID de orden a armar: "))
                    except ValueError:
                        print("ID inválido.")
                        continue
                    orden = next((o for o in ordenes_confirmadas if o.id_orden == oid), None)
                    if not orden:
                        print("Orden no encontrada o no está confirmada.")
                        continue
                    agente.armar_pedido(orden)

                elif opcion_agente == "4":
                    ordenes_empaquetadas = [o for o in ordenes_global if o.estado == "Empaquetado"]
                    if not ordenes_empaquetadas:
                        print("No hay órdenes empaquetadas para asignar transporte.")
                        continue
                    try:
                        oid = int(input("Ingrese ID de orden a enviar: "))
                    except ValueError:
                        print("ID inválido.")
                        continue
                    orden = next((o for o in ordenes_empaquetadas if o.id_orden == oid), None)
                    if not orden:
                        print("Orden no encontrada o no está empaquetada.")
                        continue
                    agente.seleccionar_transporte(transportadora, orden)

                elif opcion_agente == "5":
                    print("Cerrando sesión de Agente de Depósito.")
                    break

                else:
                    print("Opción inválida, inténtelo de nuevo.")

            continue
        elif rol == "3":

            print(f"Acceso concedido Gerente de Relaciones: {nombre} ({correo})")

            while True:
                print("\nMenú Gerente de Relaciones:")
                print("1. Ver todas las quejas")
                print("2. Responder una queja")
                print("3. Cerrar sesión de gerente")
                eleccion = input("Elija opción: ").strip()

                if eleccion == "1":
                    gerente.leer_quejas(lista_quejas)
                elif eleccion == "2":
                    if not lista_quejas:
                        print("No hay quejas para responder.")
                        continue
                    try:
                        qid = int(input("Ingrese ID de queja a responder: "))
                    except ValueError:
                        print("ID inválido, debe ser un número.")
                        continue
                    queja_sel = next((q for q in lista_quejas if q.id_queja == qid), None)
                    if not queja_sel:
                        print("Queja no encontrada.")
                        continue
                    respuesta = input("Ingrese la respuesta del gerente: ")
                    gerente.responder_queja(queja_sel, respuesta)
                elif eleccion == "3":
                    print("Saliendo de sesión gerente y volviendo a selección de rol.")
                    break
                else:
                    print("Opción inválida, inténtelo de nuevo.")

            continue

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
                            ordenes_global.append(orden)  # Agregar a la lista global para que el agente pueda consultarla
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
                lista_quejas.append(queja)
                queja.enviar_a_gerente(gerente)
            elif opcion == "9":
                print("Sesión cerrada. Volviendo al menú principal de roles.")
                break
            else:
                print("Opción inválida, inténtelo de nuevo.")

    # Fin del flujo de un rol; seguimos en el bucle principal para reautenticación

if __name__ == "__main__":
    # PEP 8: configuración de path para ejecución directa
    import os
    import sys
    pkg_dir = os.path.dirname(os.path.abspath(__file__))
    parent = os.path.dirname(pkg_dir)
    if parent not in sys.path:
        sys.path.insert(0, parent)
    app()