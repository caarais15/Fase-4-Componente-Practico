# Actividad: Fase 4 - Componente Práctico
# Ejercicio: Sistema integral de gestión de clientes, servicios y reservas
# Estudiante: María de los Ángeles Henao Manrique
# Grupo: 213023_356
# Programa: Ingeniería Multimedia
# Código fuente: Autoría propia

"""Configuración del archivo de logs (única persistencia permitida)."""
import logging  # Módulo estándar de registro de eventos
import os  # Crea la carpeta de logs

# Ruta de la carpeta y del archivo de logs
RUTA_LOGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "eventos.log")

def obtener_logger() -> logging.Logger:
    """Devuelve el logger de la aplicación, creándolo una sola vez."""
    os.makedirs(RUTA_LOGS, exist_ok=True)  # Crea la carpeta en caso de que no exista
    logger = logging.getLogger("software_fj")  # Logger con nombre propio

    if not logger.handlers:  # Evita duplicar manejadores si se llama nuevamente
        logger.setLevel(logging.INFO)  # Registra los datos INFO, WARNING y ERROR
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # Escribe en archivo
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s"  # Corresponde a FECHA, NIVEL y MENSAJE
        )
        manejador.setFormatter(formato)  # Aplica el formato
        logger.addHandler(manejador)  # Conecta el manejador
    return logger

# Instancia global reutilizada por todos los módulos
log = obtener_logger()
