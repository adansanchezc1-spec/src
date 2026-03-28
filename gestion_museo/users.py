# users.py
from abc import ABC
from datetime import date
from typing import List
from inventory import Obra_Arte, Sala
from operations import Restauracion, Cesion, Museo_Colaborador
from enums import EstadoObra
from factories import ObraFactory


class Usuario(ABC):
    """Clase base abstracta para todos los roles."""

    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password

    @property
    def username(self) -> str:
        """Nombre de usuario (solo lectura)."""
        return self._username

    def autenticar(self, password: str) -> bool:
        """Valida credenciales."""
        return self._password == password


class Encargado_Catalogo(Usuario):
    """Rol responsable de registrar nuevas obras."""

    def inscribir_obra(self, catalogo: List[Obra_Arte], obra: Obra_Arte) -> None:
        """Inscribe una obra en el catálogo."""
        catalogo.append(obra)
        print(f"[Catálogo] Obra '{obra.titulo}' inscrita exitosamente.")

    def asignar_estado(self, obra: Obra_Arte, estado: EstadoObra) -> None:
        """Asigna un estado a una obra."""
        obra.cambiar_estado(estado)
        print(f"[Catálogo] Estado de '{obra.titulo}' cambiado a: {estado.value}.")

    def mostrar_menu(self) -> None:
        """Muestra las opciones del encargado del catálogo."""
        print("\n--- MENÚ ENCARGADO CATALOGO ---")
        print("1. Registrar obra")
        print("2. Consultar catálogo")
        print("3. Cambiar estado de obra")
        print("4. Salir")

    def introducir_obra(self, catalogo: List[Obra_Arte], tipo: str, **kwargs) -> Obra_Arte:
        """Registra una nueva obra usando la fábrica."""
        nueva_obra = ObraFactory.crear_obra(tipo, **kwargs)
        self.inscribir_obra(catalogo, nueva_obra)
        return nueva_obra


class Restaurador_Jefe(Usuario):
    """Rol responsable de restauraciones y mantenimiento."""

    def iniciar_restauracion(self, obra: Obra_Arte, fecha_inicio: date, tipo: str = "Correctiva", causa: str = "Reparación solicitada") -> None:
        """Inicia una restauración sobre una obra."""
        if obra.estado == EstadoObra.RESTAURACION:
            print(f"[Restauración] La obra '{obra.titulo}' ya está en restauración.")
            return

        obra.cambiar_estado(EstadoObra.RESTAURACION)
        nueva_restauracion = Restauracion(tipo, fecha_inicio, causa)
        obra.registrar_restauracion(nueva_restauracion)
        print(f"[Restauración] '{obra.titulo}' ingresada por: {causa}")

    def enviar_a_restauracion(self, obra: Obra_Arte, tipo: str = "Correctiva", causa: str = "Daño reportado") -> None:
        """Atiende un daño urgente y comienza restauración instantánea."""
        self.iniciar_restauracion(obra, date.today(), tipo, causa)

    def proceso_diario_mantenimiento(self, catalogo: List[Obra_Arte]) -> None:
        """Verifica automáticamente obras que requieren mantenimiento cada 5 años."""
        hoy = date.today()
        for obra in catalogo:
            if obra.estado == EstadoObra.EXPUESTA and obra.requiere_mantenimiento_quinquenal(hoy):
                print(f"[Alerta Automática] '{obra.titulo}' requiere mantenimiento preventivo (Han pasado 5 años).")
                self.enviar_a_restauracion(obra, "Preventiva", "Mantenimiento 5 años")

    def consultar_restauraciones(self, obra: Obra_Arte) -> None:
        """Muestra historial ordenado por fecha."""
        ordenadas = sorted(
            obra.obtener_historial_restauraciones(), key=lambda r: r.fecha_inicio
        )
        print(f"--- Historial de '{obra.titulo}' ---")
        for r in ordenadas:
            fin = r.fecha_fin if r.fecha_fin else "En curso"
            print(f"- Inicio: {r.fecha_inicio} | Fin: {fin} | Tipo: {r.tipo} | Causa: {r.causa}")


class Director_Museo(Usuario):
    """Rol responsable de valoración y cesiones."""

    def consultar_valoracion_total(self, catalogo: List[Obra_Arte]) -> float:
        """Calcula y muestra el valor total del inventario."""
        total = sum(obra.valoracion for obra in catalogo)
        print(f"[Director] Valoración total del museo: ${total:,.2f}")
        return total

    def gestionar_cesion(
        self, obra: Obra_Arte, museo: Museo_Colaborador, importe: float, dias: int
    ) -> None:
        """Gestiona una cesión y actualiza estado en cola."""
        nueva_cesion = Cesion(museo, importe, dias, date.today())
        obra.agregar_cesion(nueva_cesion)

        mensaje = f"[Cesión] '{obra.titulo}' agregada para {museo.nombre} por {dias} días. Importe: ${importe:,.2f}"
        if obra.estado == EstadoObra.CEDIDA and obra.obtener_cesion_actual() == nueva_cesion:
            mensaje = f"[Cesión] '{obra.titulo}' cedida actualmente a {museo.nombre} por {dias} días."
        elif obra.estado == EstadoObra.CEDIDA:
            mensaje = f"[Cesión] '{obra.titulo}' está en cesión; la nueva cesión a {museo.nombre} queda en cola."

        print(mensaje)


class Visitante:
    """Actor pasivo. Solo consulta el monitor."""

    @staticmethod
    def consultar_monitor_por_sala(sala: Sala) -> None:
        """Muestra obras expuestas en la sala indicada."""
        print(f"\n=== MONITOR VESTÍBULO: {sala.nombre} ===")
        for obra in sala.obtener_obras_expuestas():
            print(f"- {obra.obtener_ficha()}")