# Software FJ - Sistema de gestión de clientes, servicios y reservas

Proyecto POO en Python (curso Programación 213023, UNAD). Sin base de datos: usa objetos, listas y un archivo de logs.

## Ejecución
```
python main.py
```
Los eventos y errores quedan en `logs/eventos.log`.

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Jerarquía de excepciones personalizadas |
| `logger.py` | Configuración del archivo de logs |
| `entidad.py` | Clase abstracta `Entidad` |
| `cliente.py` | `Cliente` con encapsulación y validaciones |
| `servicio.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `Asesoria` |
| `reserva.py` | `Reserva`: confirmar, cancelar, procesar |
| `main.py` | Simulación de 14 operaciones válidas e inválidas |

## Conceptos aplicados
- Abstracción: `Entidad` y `Servicio` (ABC, métodos abstractos).
- Herencia y polimorfismo: tres servicios sobrescriben `costo_base`, `describir` y `validar_parametros`.
- Encapsulación: atributos privados con `@property` y validación en setters.
- Sobrecarga: `calcular_costo` acepta descuento numérico, código promocional o parámetros con nombre.
- Excepciones: `try/except`, `try/except/else`, `try/except/finally` y encadenamiento (`raise ... from e`).
# Fase-4-Componente-Practico
