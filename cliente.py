"""Clase Cliente con encapsulación y validaciones robustas."""
import re  # expresiones regulares para validar el correo

from entidad import Entidad
from excepciones import ClienteInvalidoError, DatosFaltantesError

# Patrón simple de correo: texto@dominio.extensión
PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Cliente(Entidad):
    """Cliente de Software FJ. Sus datos personales son privados."""

    def __init__(self, nombre=None, correo=None, telefono=None, documento=None):
        super().__init__()  # asigna el id de la Entidad
        # Cada campo pasa por su setter, que valida y lanza excepciones
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.documento = documento

    # ---------- nombre ----------
    @property
    def nombre(self) -> str:
        return self.__nombre  # atributo privado (name mangling)

    @nombre.setter
    def nombre(self, valor):
        if valor is None:  # parámetro faltante
            raise DatosFaltantesError("El nombre del cliente es obligatorio.")
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError(f"Nombre inválido: {valor!r} (mínimo 3 letras).")
        if any(c.isdigit() for c in valor):
            raise ClienteInvalidoError("El nombre no puede contener números.")
        self.__nombre = valor.strip().title()  # normaliza el formato

    # ---------- correo ----------
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None:
            raise DatosFaltantesError("El correo del cliente es obligatorio.")
        if not isinstance(valor, str) or not PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}.")
        self.__correo = valor.strip().lower()

    # ---------- teléfono ----------
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None:
            raise DatosFaltantesError("El teléfono del cliente es obligatorio.")
        texto = str(valor).strip()
        if not texto.isdigit() or len(texto) != 10:  # celular colombiano: 10 dígitos
            raise ClienteInvalidoError(f"Teléfono inválido: {valor!r} (10 dígitos).")
        self.__telefono = texto

    # ---------- documento ----------
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None:
            raise DatosFaltantesError("El documento del cliente es obligatorio.")
        texto = str(valor).strip()
        if not texto.isdigit() or not (6 <= len(texto) <= 10):
            raise ClienteInvalidoError(f"Documento inválido: {valor!r} (6 a 10 dígitos).")
        self.__documento = texto

    def describir(self) -> str:
        """Implementación del método abstracto de Entidad."""
        return f"Cliente #{self.id}: {self.nombre} <{self.correo}> Tel. {self.telefono}"
