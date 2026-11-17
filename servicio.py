# Actividad: Fase 4 - Componente Práctico
# Ejercicio: Sistema integral de gestión de clientes, servicios y reservas
# Estudiante: María de los Ángeles Henao Manrique
# Grupo: 213023_356
# Programa: Ingeniería Multimedia
# Código fuente: Autoría propia

"""Clase abstracta Servicio y tres servicios especializados (polimorfismo)."""
from abc import abstractmethod  # Decorador para métodos abstractos

from entidad import Entidad
from excepciones import (
    CalculoInconsistenteError,
    ServicioInvalidoError,
)

IVA = 0.19  # Impuesto por defecto del 19 %

class Servicio(Entidad):
    """Servicio genérico de Software FJ (abstracto)."""

    def __init__(self, nombre: str, tarifa_hora: float, disponible: bool = True):
        super().__init__()  # Asigna un ID
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}.")
        self._nombre = nombre.strip()  # Nombre del servicio
        self._tarifa_hora = float(tarifa_hora)  # Valor por hora
        self._disponible = bool(disponible)  # Si puede reservarse

    @property
    def nombre(self) -> str:
        """Devuelve el nombre del servicio."""
        return self._nombre

    @property
    def tarifa_hora(self) -> float:
        """Devuelve la tarifa por hora del servicio."""
        return self._tarifa_hora

    @property
    def disponible(self) -> bool:
        """Indica si el servicio está disponible para reservar."""
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)  # Permite habilitar y/o deshabilitar

    # Métodos abstractos (cada hijo los sobrescribe)
    @abstractmethod
    def validar_parametros(self, duracion_horas) -> None:
        """Valida la duración solicitada según las reglas de cada servicio."""

    @abstractmethod
    def costo_base(self, duracion_horas: float) -> float:
        """Costo sin impuestos ni descuentos (varía en cada servicio)."""

    # Método SOBRECARGADO de cálculo de costos
    def calcular_costo(self, duracion_horas, *opciones, impuesto: float = IVA,
                       descuento: float = 0.0) -> float:
        """Calcula el costo final. Admite varias variantes de llamada:

        - calcular_costo(2)                  -> con IVA por defecto
        - calcular_costo(2, 0.10)            -> con 10 % de descuento
        - calcular_costo(2, "PROMO10")       -> con código promocional
        - calcular_costo(2, impuesto=0)      -> sin impuesto
        - calcular_costo(2, descuento=0.2, impuesto=0.05)
        """
        for op in opciones:  # Variante posicional: tipo de dato decide el significado
            if isinstance(op, str):  # Código promocional
                descuento = {"PROMO10": 0.10, "PROMO20": 0.20}.get(op.upper(), -1)
                if descuento < 0:
                    raise ServicioInvalidoError(f"Código promocional desconocido: {op!r}.")
            elif isinstance(op, (int, float)):  # Descuento numérico
                descuento = float(op)
            else:
                raise ServicioInvalidoError(f"Opción no soportada: {op!r}.")
        self.validar_parametros(duracion_horas)  # Reglas del servicio concreto
        if not (0 <= descuento < 1) or not 0 <= impuesto < 1:
            raise CalculoInconsistenteError("Descuento o impuesto fuera de rango [0, 1)")
        base = self.costo_base(duracion_horas)  # Polimorfismo: depende del hijo
        total = base * (1 - descuento) * (1 + impuesto)  # Aplica descuento e impuesto
        if total <= 0:  # Resultado incoherente
            raise CalculoInconsistenteError(f"Costo calculado no válido: {total}")
        return round(total, 2)


class ReservaSala(Servicio):
    """Reserva de salas de reuniones (capacidad limitada)."""

    def __init__(self, nombre: str, tarifa_hora: float, capacidad: int, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion_horas) -> None:
        # Una sala se reserva entre 1 y 8 horas
        if not isinstance(duracion_horas, (int, float)) or not 1 <= duracion_horas <= 8:
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas.")

    def costo_base(self, duracion_horas: float) -> float:
        return self._tarifa_hora * duracion_horas  # tarifa lineal

    def describir(self) -> str:
        return (f"Sala '{self.nombre}' (capacidad {self._capacidad}) - "
                f"${self.tarifa_hora:,.0f}/h")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos tecnológicos, con recargo de seguro."""

    def __init__(self, nombre: str, tarifa_hora: float, tipo_equipo: str, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not tipo_equipo or not str(tipo_equipo).strip():
            raise ServicioInvalidoError("Debe indicar el tipo de equipo")
        self._tipo_equipo = str(tipo_equipo).strip()

    def validar_parametros(self, duracion_horas) -> None:
        # Equipos: de 1 hasta 72 horas (3 días)
        if not isinstance (duracion_horas, (int, float)) or not 1 <= duracion_horas <= 72:
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas.")

    def costo_base(self, duracion_horas: float) -> float:
        return self._tarifa_hora * duracion_horas * 1.05  # +5 % por seguro

    def describir(self) -> str:
        return (f"Equipo '{self.nombre}' tipo {self._tipo_equipo} - "
                f"${self.tarifa_hora:,.0f}/h (+5 % seguro)")


class Asesoria(Servicio):
    """Asesoría especializada, con recargo según el nivel del experto."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}  # multiplicadores

    def __init__(self, nombre: str, tarifa_hora: float, nivel: str, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if str(nivel).lower() not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel inválido: {nivel!r}. Use {list(self.NIVELES)}.")
        self._nivel = str(nivel).lower()

    def validar_parametros(self, duracion_horas) -> None:
        # Asesorías: entre 0.5 y 6 horas
        if not isinstance(duracion_horas, (int, float)) or not 0.5 <= duracion_horas <= 6:
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 6 horas.")

    def costo_base(self, duracion_horas: float) -> float:
        return self._tarifa_hora * duracion_horas * self.NIVELES[self._nivel]

    def describir(self) -> str:
        return f"Asesoría '{self.nombre}' nivel {self._nivel} - ${self.tarifa_hora:,.0f}/h"
