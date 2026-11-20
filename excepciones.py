"""Excepciones personalizadas del sistema Software FJ.

Se define una jerarquía: todas heredan de SoftwareFJError, de modo que
el programa pueda capturar cualquier error propio con un único except.
"""


class SoftwareFJError(Exception):
    """Excepción base de la aplicación Software FJ."""


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no superan las validaciones."""


class DatosFaltantesError(SoftwareFJError):
    """Se lanza cuando falta un parámetro obligatorio."""


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los parámetros de un servicio son incorrectos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando se intenta reservar un servicio no disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva se crea con datos incorrectos."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando se intenta una operación no válida para el estado actual."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo de costos produce un resultado incoherente."""
