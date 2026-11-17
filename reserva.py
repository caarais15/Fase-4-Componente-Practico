# Actividad: Fase 4 - Componente Práctico
# Ejercicio: Sistema integral de gestión de clientes, servicios y reservas
# Estudiante: María de los Ángeles Henao Manrique
# Grupo: 213023_356
# Programa: Ingeniería Multimedia
# Código fuente: Autoría propia

"""Clase Reserva: integra cliente, servicio, duración y estado."""
from cliente import Cliente
from entidad import Entidad
from excepciones import (
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    SoftwareFJError,
)
from logger import log
from servicio import Servicio

# Estados posibles de una reserva
PENDIENTE, CONFIRMADA, CANCELADA = "PENDIENTE", "CONFIRMADA", "CANCELADA"

class Reserva(Entidad):
    """Reserva de un servicio por parte de un cliente."""

    def __init__(self, cliente, servicio, duracion_horas):
        super().__init__()
        # Validación de tipos que evita objetos incorrectos
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido.")
        # Un servicio no disponible no puede reservarse
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible.")
        try:  # try/except con encadenamiento de excepciones
            servicio.validar_parametros(duracion_horas)
        except ServicioInvalidoError as e:
            # 'from e' conserva la causa original (encadenamiento)
            raise ReservaInvalidaError(f"Duración inválida: {duracion_horas!r}.") from e
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion_horas
        self._estado = PENDIENTE  # Toda reserva nace pendiente

    @property
    def estado(self) -> str:
        """Devuelve el estado actual de la reserva."""
        return self._estado

    @property
    def cliente(self) -> Cliente:
        """Devuelve el cliente asociado a la reserva."""
        return self._cliente

    @property
    def servicio(self) -> Servicio:
        """Devuelve el servicio asociado a la reserva."""
        return self._servicio

    def confirmar(self) -> None:
        """Pasa la reserva de PENDIENTE a CONFIRMADA."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva {self._estado}.")
        if not self._servicio.disponible:  # Puede haberse deshabilitado después
            raise ServicioNoDisponibleError(f"'{self._servicio.nombre}' ya no está disponible.")
        self._estado = CONFIRMADA
        log.info("Reserva #%s confirmada.", self.id)

    def cancelar(self) -> None:
        """Cancela una reserva que no esté ya cancelada."""
        if self._estado == CANCELADA:
            raise OperacionNoPermitidaError("La reserva ya estaba cancelada.")
        self._estado = CANCELADA
        log.info("Reserva #%s cancelada.", self.id)

    def procesar(self, **opciones_costo) -> float:
        """Confirma la reserva y devuelve el costo total.

        Usa try/except/else/finally y encadenamiento de excepciones.
        """
        costo = None
        estado_previo = self._estado  # para revertir si el cálculo falla
        try:
            self.confirmar()  # Puede lanzar OperacionNoPermitida / NoDisponible
            costo = self._servicio.calcular_costo(self._duracion, **opciones_costo)
        except SoftwareFJError as e:
            self._estado = estado_previo  # Revierte y no queda confirmada sin costo
            # Se registra y se relanza con contexto
            log.error("Fallo al procesar reserva #%s: %s", self.id, e)
            raise OperacionNoPermitidaError(
                f"No fue posible procesar la reserva #{self.id}.") from e
        except Exception as e:  # Error inesperado
            self._estado = estado_previo
            log.error("Error inesperado en reserva #%s: %r", self.id, e)
            raise OperacionNoPermitidaError("Error interno al procesar.") from e
        else:  # Solo se ejecuta si no hubo excepción
            log.info("Reserva #%s procesada. Costo total: $%s", self.id, f"{costo:,.2f}")
            return costo
        finally:  # siempre se ejecuta
            log.info("Fin del procesamiento de la reserva #%s (estado %s).",
                     self.id, self._estado)

    def describir(self) -> str:
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} ({self._duracion} h)")
