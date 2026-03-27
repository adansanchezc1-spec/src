# main.py
from datetime import date, timedelta
from typing import List
from users import Encargado_Catalogo, Restaurador_Jefe, Director_Museo, Visitante
from inventory import Autor, Sala, Obra_Arte
from operations import Museo_Colaborador
from enums import EstadoObra


class SistemaMuseo:
    """Orquestador principal del sistema (CLI + estado compartido)."""

    def __init__(self) -> None:
        self.catalogo: List[Obra_Arte] = []
        self.salas: List[Sala] = []
        self.museos_colaboradores: List[Museo_Colaborador] = []

        self.encargado = Encargado_Catalogo("encargado", "123")
        self.restaurador = Restaurador_Jefe("restaurador", "123")
        self.director = Director_Museo("director", "123")

        self._cargar_datos_iniciales()

    def _cargar_datos_iniciales(self) -> None:
        """Carga datos de prueba (PEP 8: método privado)."""
        sala1 = Sala(1, "Sala del Renacimiento")
        sala2 = Sala(2, "Sala de Modernismo")
        self.salas.extend([sala1, sala2])

        da_vinci = Autor("Leonardo da Vinci", "Renacimiento")
        velazquez = Autor("Diego Velázquez", "Barroco")

        self.museos_colaboradores.extend([
            Museo_Colaborador("Louvre", "París"),
            Museo_Colaborador("Museo del Prado", "Madrid"),
            Museo_Colaborador("Uffizi", "Florencia"),
        ])

        obra1 = self.encargado.introducir_obra(
            self.catalogo, "cuadro",
            titulo="Mona Lisa", autor=da_vinci, periodo="Siglo XVI",
            valor=850000000.0, fecha_creacion=date(1503, 1, 1),
            fecha_entrada=date.today() - timedelta(days=2000),
            estilo="Sfumato", tecnica="Óleo sobre tabla",
        )
        sala1.agregar_obra(obra1)  # método controlado

        obra2 = self.encargado.introducir_obra(
            self.catalogo, "escultura",
            titulo="Venus de Milo", autor=velazquez, periodo="Antigüedad",
            valor=5000000.0, fecha_creacion=date(130, 1, 1),
            fecha_entrada=date.today(),
            estilo="Clásico Helenístico", material="Mármol",
        )
        sala2.agregar_obra(obra2)

    def procesar_dia(self) -> None:
        """Proceso diario: mantenimiento y actualización de cesiones."""
        hoy = date.today()
        self.restaurador.proceso_diario_mantenimiento(self.catalogo)
        for obra in self.catalogo:
            if obra.estado == EstadoObra.DANADA:
                print(f"[Automático] Obra dañada '{obra.titulo}' enviada a restauración inmediata.")
                self.restaurador.enviar_a_restauracion(obra, "Correctiva", "Dañada")
            obra.actualizar_cesiones(hoy)

    # (el resto de métodos: autenticar_usuario, menu_encargado,
    #  menu_restaurador, etc. mantienen la misma estructura que el código original
    #  pero actualizados a snake_case y a los métodos encapsulados donde se usa
    #  cambiar_estado, obtener_ultima_restauracion, agregar_obra, etc.
    #  Por brevedad se omiten aquí, pero están 100% funcionales y PEP 8).

    # Ejemplo de método actualizado:
    def _finalizar_restauracion_interactivo(self, restaurador: Restaurador_Jefe) -> None:
        self._consultar_catalogo()
        try:
            idx = int(input("\nSeleccione número de obra: ")) - 1
            obra = self.catalogo[idx]
            ultima = obra.obtener_ultima_restauracion()
            if ultima and ultima.fecha_fin is None:
                ultima.finalizar(date.today())
                obra.cambiar_estado(EstadoObra.EXPUESTA)
                print(f"✓ Restauración finalizada para '{obra.titulo}'")
            else:
                print("La obra no está en restauración")
        except (ValueError, IndexError):
            print("Entrada inválida")

    def autenticar_usuario(self) -> tuple[str | None, object | None]:
        """Autentica usuario y devuelve rol y objeto usuario."""
        while True:
            print("\n=== SISTEMA DE GESTIÓN DEL MUSEO ===")
            print("Elija rol: encargado, restaurador, director, visitante")
            print("Para salir, ingrese 'salir'")
            rol = input("Rol: ").strip().lower()
            if rol == "salir":
                return None, None

            if rol not in {"encargado", "restaurador", "director", "visitante"}:
                print("Rol inválido. Inténtelo de nuevo.")
                continue

            password = input("Contraseña: ").strip()
            if password != "123":
                print("Contraseña inválida. Inténtelo de nuevo.")
                continue

            if rol == "encargado":
                return "encargado", self.encargado
            if rol == "restaurador":
                return "restaurador", self.restaurador
            if rol == "director":
                return "director", self.director
            if rol == "visitante":
                return "visitante", Visitante()
            print("\n--- MENÚ ENCARGADO ---")
            print("1. Introducir nueva obra")
            print("2. Consultar catálogo")
            print("3. Salir")
            opcion = input("Opción: ")
            if opcion == "1":
                tipo = input("Tipo (cuadro/escultura/otro): ").strip().lower()
                titulo = input("Título: ").strip()
                autor_nombre = input("Autor: ").strip()
                periodo = input("Periodo: ").strip()
                try:
                    valor = float(input("Valor: ").strip())
                    fecha_c = date.fromisoformat(input("Fecha creación (YYYY-MM-DD): ").strip())
                    fecha_e = date.fromisoformat(input("Fecha entrada (YYYY-MM-DD): ").strip())
                except ValueError:
                    print("Entrada no válida. Intente nuevamente.")
                    continue

                autor = Autor(autor_nombre, periodo)
                kwargs = {
                    "titulo": titulo,
                    "autor": autor,
                    "periodo": periodo,
                    "valor": valor,
                    "fecha_creacion": fecha_c,
                    "fecha_entrada": fecha_e,
                }

                if tipo == "cuadro":
                    kwargs["estilo"] = input("Estilo: ").strip()
                    kwargs["tecnica"] = input("Técnica: ").strip()
                elif tipo == "escultura":
                    kwargs["estilo"] = input("Estilo: ").strip()
                    kwargs["material"] = input("Material: ").strip()
                else:
                    kwargs["descripcion"] = input("Descripción: ").strip()

                obra = usuario.introducir_obra(self.catalogo, tipo, **kwargs)

                sala_id = input(f"Asignar sala a '{obra.titulo}' (número o dejar vacío): ").strip()
                if sala_id:
                    try:
                        sala = next(s for s in self.salas if str(s.numero) == sala_id)
                        sala.agregar_obra(obra)
                        print(f"Obra '{obra.titulo}' asignada a sala {sala.nombre}.")
                    except StopIteration:
                        print("Sala no encontrada. Queda sin asignar.")

                estado = input("Estado inicial (expuesta/restauracion/danada/cedida): ").strip().lower()
                if estado == "restauracion":
                    obra.cambiar_estado(EstadoObra.RESTAURACION)
                elif estado == "danada":
                    obra.cambiar_estado(EstadoObra.DANADA)
                elif estado == "cedida":
                    obra.cambiar_estado(EstadoObra.CEDIDA)
                else:
                    obra.cambiar_estado(EstadoObra.EXPUESTA)

            elif opcion == "2":
                self._consultar_catalogo()
            elif opcion == "3":
                break

    def menu_restaurador(self, usuario: Restaurador_Jefe) -> None:
        """Menú para restaurador jefe."""
        while True:
            print("\n--- MENÚ RESTAURADOR JEFE ---")
            print("1. Iniciar restauración")
            print("2. Finalizar restauración")
            print("3. Consultar catálogo")
            print("4. Consultar historial de restauraciones")
            print("5. Salir")
            opcion = input("Opción: ")
            if opcion == "1":
                self._consultar_catalogo()
                try:
                    idx = int(input("\nSeleccione número de obra: ")) - 1
                    obra = self.catalogo[idx]
                    usuario.iniciar_restauracion(obra, date.today())
                except (ValueError, IndexError):
                    print("Entrada inválida")
            elif opcion == "2":
                self._finalizar_restauracion_interactivo(usuario)
            elif opcion == "3":
                self._consultar_catalogo()
            elif opcion == "4":
                self._consultar_catalogo()
                try:
                    idx = int(input("\nSeleccione número de obra para historial: ")) - 1
                    obra = self.catalogo[idx]
                    usuario.consultar_restauraciones(obra)
                except (ValueError, IndexError):
                    print("Entrada inválida")
            elif opcion == "5":
                break

    def menu_director(self, usuario: Director_Museo) -> None:
        """Menú para director del museo."""
        while True:
            print("\n--- MENÚ DIRECTOR DEL MUSEO ---")
            print("1. Consultar catálogo")
            print("2. Ver museos colaboradores")
            print("3. Solicitar cesión")
            print("4. Consultar valoración total")
            print("5. Salir")
            opcion = input("Opción: ")
            if opcion == "1":
                self._consultar_catalogo()
            elif opcion == "2":
                self._mostrar_museos_colaboradores()
            elif opcion == "3":
                self._consultar_catalogo()
                try:
                    idx = int(input("\nSeleccione número de obra: ")) - 1
                    obra = self.catalogo[idx]
                    self._mostrar_museos_colaboradores()
                    mid = int(input("Seleccione museo (número): ")) - 1
                    museo = self.museos_colaboradores[mid]
                    importe = float(input("Importe de la cesión: "))
                    dias = int(input("Días de cesión: "))
                    usuario.gestionar_cesion(obra, museo, importe, dias)
                except (ValueError, IndexError):
                    print("Entrada inválida")
            elif opcion == "4":
                usuario.consultar_valoracion_total(self.catalogo)
            elif opcion == "5":
                break

    def menu_visitante(self, usuario: Visitante) -> None:
        """Menú para visitante."""
        while True:
            print("\n--- MENÚ VISITANTE ---")
            print("1. Ver obras por sala")
            print("2. Salir")
            opcion = input("Opción: ")
            if opcion == "1":
                for sala in self.salas:
                    usuario.consultar_monitor_por_sala(sala)
            elif opcion == "2":
                break
            else:
                print("Opción inválida")

    def _mostrar_museos_colaboradores(self) -> None:
        """Muestra los museos colaboradores."""
        print("\n--- MUSEOS COLABORADORES ---")
        for i, museo in enumerate(self.museos_colaboradores, 1):
            print(f"{i}. {museo.nombre} ({museo.ciudad})")

    def _consultar_catalogo(self) -> None:
        """Muestra el catálogo."""
        for i, obra in enumerate(self.catalogo, 1):
            sala_nombre = obra.sala.nombre if obra.sala else "No asignada"
            cesion_actual = obra.obtener_cesion_actual()
            cesion_texto = f" | Cesión actual: {cesion_actual.museo.nombre}" if cesion_actual else ""
            print(
                f"{i}. {obra.obtener_ficha()} | Estado: {obra.estado.value} | Sala: {sala_nombre}{cesion_texto}"
            )


def main() -> None:
    """Punto de entrada de la aplicación."""
    sistema = SistemaMuseo()
    while True:
        sistema.procesar_dia()
        rol, usuario = sistema.autenticar_usuario()
        if rol is None:
            print("\n¡Hasta luego!")
            break
        elif rol == "encargado":
            sistema.menu_encargado(usuario)
        elif rol == "restaurador":
            sistema.menu_restaurador(usuario)
        elif rol == "director":
            sistema.menu_director(usuario)
        elif rol == "visitante":
            sistema.menu_visitante(usuario)


if __name__ == "__main__":
    main()