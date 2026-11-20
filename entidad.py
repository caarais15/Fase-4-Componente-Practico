"""Clase abstracta que representa las entidades generales del sistema."""
from abc import ABC, abstractmethod  # herramientas para clases abstractas
import itertools  # contador para generar identificadores únicos


class Entidad(ABC):
    """Entidad general: toda clase del dominio tiene un id y se describe."""

    _contador = itertools.count(1)  # generador compartido de identificadores

    def __init__(self):
        self._id = next(Entidad._contador)  # asigna el siguiente id disponible

    @property
    def id(self) -> int:
        """Identificador único (solo lectura: encapsulación)."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Devuelve una descripción legible; cada subclase la implementa."""

    def __str__(self) -> str:
        return self.describir()  # str(obj) usa la descripción polimórfica
