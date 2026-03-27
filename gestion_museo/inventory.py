# inventory.py
# PEP 8: Imports ordenados (stdlib → locales)
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List
from enums import EstadoObra
from operations import Restauracion, Cesion


class Autor:
    """Representa al autor de una obra de arte."""

    def __init__(self, nombre: str, periodo_historico: str) -> None:
        self._nombre = nombre
        self._periodo_historico = periodo_historico

    @property
    def nombre(self) -> str:
        """Nombre del autor (solo lectura)."""
        return self._nombre

    @property
    def periodo_historico(self) -> str:
        """Período histórico del autor (solo lectura)."""
        return self._periodo_historico


class Sala:
    """Espacio físico del museo donde se exponen obras."""

    def __init__(self, numero: int, nombre: str) -> None:
        self._numero = numero
        self._nombre = nombre
        self._obras_expuestas: List["Obra_Arte"] = []  # privado

    @property
    def numero(self) -> int:
        """Número de la sala (solo lectura)."""
        return self._numero

    @property
    def nombre(self) -> str:
        """Nombre de la sala (solo lectura)."""
        return self._nombre

    def agregar_obra(self, obra: "Obra_Arte") -> None:
        """Método público controlado para agregar obras (encapsulamiento)."""
        self._obras_expuestas.append(obra)
        obra.asignar_sala(self)
        obra.cambiar_estado(EstadoObra.EXPUESTA)

    def obtener_obras_expuestas(self) -> List["Obra_Arte"]:
        """Devuelve solo las obras realmente expuestas (copia filtrada)."""
        return [o for o in self._obras_expuestas if o.estado == EstadoObra.EXPUESTA]


class Obra_Arte(ABC):
    """Clase base abstracta para cualquier pieza del inventario."""

    def __init__(
        self,
        titulo: str,
        autor: Autor,
        periodo: str,
        valor: float,
        fecha_creacion: date,
        fecha_entrada: date,
    ) -> None:
        self._titulo = titulo
        self._autor = autor
        self._periodo = periodo
        self._valoracion = valor
        self._fecha_creacion = fecha_creacion
        self._fecha_entrada = fecha_entrada
        self._sala = None

        # Atributos encapsulados (privados)
        self._estado = EstadoObra.EXPUESTA
        self._historial_restauraciones: List[Restauracion] = []
        self._cola_cesiones: List[Cesion] = []
        self._cesion_actual: Cesion | None = None

    @property
    def titulo(self) -> str:
        """Título de la obra (solo lectura)."""
        return self._titulo

    @property
    def autor(self) -> Autor:
        """Autor de la obra (solo lectura)."""
        return self._autor

    @property
    def periodo(self) -> str:
        """Período de la obra (solo lectura)."""
        return self._periodo

    @property
    def valoracion(self) -> float:
        """Valoración de la obra (solo lectura)."""
        return self._valoracion

    @property
    def fecha_creacion(self) -> date:
        """Fecha de creación de la obra (solo lectura)."""
        return self._fecha_creacion

    @property
    def fecha_entrada(self) -> date:
        """Fecha de entrada al museo (solo lectura)."""
        return self._fecha_entrada

    @property
    def sala(self):
        """Sala donde está expuesta la obra (solo lectura)."""
        return self._sala

    def asignar_sala(self, sala) -> None:
        """Asigna la sala a la obra."""
        self._sala = sala

    def cambiar_estado(self, nuevo_estado: EstadoObra) -> None:
        """Método público controlado para cambiar estado."""
        self._estado = nuevo_estado
        if nuevo_estado == EstadoObra.CEDIDA:
            self._sala = None

    def registrar_restauracion(self, restauracion: Restauracion) -> None:
        """Registra una restauración (encapsulamiento)."""
        self._historial_restauraciones.append(restauracion)

    def agregar_cesion(self, cesion: Cesion) -> None:
        """Agrega una cesión a la cola y activa si procede."""
        self._cola_cesiones.append(cesion)
        self._iniciar_siguiente_cesion(date.today())

    def _iniciar_siguiente_cesion(self, fecha_actual: date) -> None:
        """Inicia la próxima cesión cuando no existe cesión vigente."""
        if self._cesion_actual and self._cesion_actual.esta_vigente(fecha_actual):
            return

        if self._cesion_actual and not self._cesion_actual.esta_vigente(fecha_actual):
            self._cesion_actual.finalizar(fecha_actual)
            self._cesion_actual = None
            self.cambiar_estado(EstadoObra.EXPUESTA)

        if self._cola_cesiones:
            siguiente = self._cola_cesiones.pop(0)
            self._cesion_actual = siguiente
            self.cambiar_estado(EstadoObra.CEDIDA)

    def actualizar_cesiones(self, fecha_actual: date) -> None:
        """Actualiza estado de cesiones según la fecha actual."""
        self._iniciar_siguiente_cesion(fecha_actual)

    def obtener_cesion_actual(self) -> Cesion | None:
        """Retorna la cesión activa o None."""
        return self._cesion_actual

    def esta_cedida(self) -> bool:
        """Indica si la obra está cedida."""
        return self._estado == EstadoObra.CEDIDA

    def obtener_historial_restauraciones(self) -> List[Restauracion]:
        """Devuelve copia del historial."""
        return self._historial_restauraciones[:]

    def obtener_ultima_restauracion(self) -> Restauracion | None:
        """Acceso controlado a la última restauración."""
        if self._historial_restauraciones:
            return self._historial_restauraciones[-1]
        return None

    def _obtener_ultima_fecha_mantenimiento(self) -> date | None:
        """Método privado: lógica interna de fecha de referencia."""
        if self._historial_restauraciones:
            ultima_fecha = self._historial_restauraciones[-1].fecha_fin
            if not ultima_fecha:
                return None
            return ultima_fecha
        return self.fecha_entrada

    def requiere_mantenimiento_quinquenal(self, fecha_actual: date) -> bool:
        """Verifica si han pasado 5 años desde la última restauración."""
        ultima_fecha = self._obtener_ultima_fecha_mantenimiento()
        if ultima_fecha is None:
            return False
        dias_pasados = (fecha_actual - ultima_fecha).days
        return dias_pasados >= (5 * 365)

    @abstractmethod
    def obtener_ficha(self) -> str:
        """Devuelve ficha descriptiva de la obra."""


class Cuadro(Obra_Arte):
    """Obra de tipo cuadro (hereda de Obra_Arte)."""

    def __init__(
        self,
        titulo: str,
        autor: Autor,
        periodo: str,
        valor: float,
        fecha_creacion: date,
        fecha_entrada: date,
        estilo: str,
        tecnica: str,
    ) -> None:
        super().__init__(titulo, autor, periodo, valor, fecha_creacion, fecha_entrada)
        self.estilo = estilo
        self.tecnica = tecnica

    def obtener_ficha(self) -> str:
        return f"Cuadro: {self.titulo} | Estilo: {self.estilo} | Técnica: {self.tecnica}"


class Escultura(Obra_Arte):
    """Obra de tipo escultura."""

    def __init__(
        self,
        titulo: str,
        autor: Autor,
        periodo: str,
        valor: float,
        fecha_creacion: date,
        fecha_entrada: date,
        estilo: str,
        material: str,
    ) -> None:
        super().__init__(titulo, autor, periodo, valor, fecha_creacion, fecha_entrada)
        self.estilo = estilo
        self.material = material

    def obtener_ficha(self) -> str:
        return f"Escultura: {self.titulo} | Material: {self.material}"


class Otro_Objeto(Obra_Arte):
    """Obra que no encaja en las categorías anteriores."""

    def __init__(
        self,
        titulo: str,
        autor: Autor,
        periodo: str,
        valor: float,
        fecha_creacion: date,
        fecha_entrada: date,
        descripcion: str,
    ) -> None:
        super().__init__(titulo, autor, periodo, valor, fecha_creacion, fecha_entrada)
        self.descripcion = descripcion

    def obtener_ficha(self) -> str:
        return f"Objeto: {self.titulo} | Desc: {self.descripcion}"