# support.py
from datetime import datetime


class Gerente_Relaciones:
    """Gestor de atención al cliente."""

    def __init__(self, identificacion: str) -> None:
        self.identificacion = identificacion

    def recibir_queja(self, queja: "Queja") -> None:
        """Registra recepción de queja."""
        print(f"Gerente {self.identificacion} recibió queja: {queja.motivo} (ID {queja.id_queja})")

    def gestionar_queja(self, queja: "Queja") -> None:
        """Inicia proceso de resolución."""
        print(f"Resolviendo queja {queja.id_queja} - {queja.motivo}...")

    def leer_quejas(self, quejas: list["Queja"]) -> None:
        """Muestra el listado de quejas pendientes y respondidas."""
        if not quejas:
            print("No hay quejas registradas.")
            return
        for q in quejas:
            estado = "Respondida" if q.respondida else "Pendiente"
            print(f"ID {q.id_queja} | {estado} | {q.motivo} | {q.fecha} | Respuesta: {q.respuesta or '---'}")

    def responder_queja(self, queja: "Queja", respuesta: str) -> None:
        """Marca una queja como respondida y guarda la respuesta."""
        queja.responder(respuesta)
        print(f"Queja ID {queja.id_queja} respondida.")


class Queja:
    """Registro de reclamación de cliente."""

    _contador = 1

    def __init__(self, motivo: str, descripcion: str) -> None:
        self.id_queja = Queja._contador
        Queja._contador += 1
        self._motivo = motivo
        self._descripcion_detallada = descripcion
        self._fecha = datetime.now()
        self._respuesta = None
        self._respondida = False

    @property
    def motivo(self) -> str:
        """Motivo de la queja (solo lectura)."""
        return self._motivo

    @property
    def descripcion_detallada(self) -> str:
        """Descripción completa (solo lectura)."""
        return self._descripcion_detallada

    @property
    def fecha(self) -> datetime:
        """Fecha de creación de la queja."""
        return self._fecha

    @property
    def respuesta(self) -> str | None:
        """Respuesta dada por el gerente (si existe)."""
        return self._respuesta

    @property
    def respondida(self) -> bool:
        """Indica si la queja ya fue respondida."""
        return self._respondida

    def responder(self, respuesta: str) -> None:
        """Registra la respuesta y marca como respondida."""
        self._respuesta = respuesta
        self._respondida = True

    def enviar_a_gerente(self, gerente: Gerente_Relaciones) -> None:
        """Envía la queja al gerente correspondiente."""
        gerente.recibir_queja(self)