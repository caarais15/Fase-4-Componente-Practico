"""Software FJ - Sistema integral de gestión de clientes, servicios y reservas.

Simula 12 operaciones (válidas e inválidas) sin base de datos. Los errores se
registran en logs/eventos.log y el programa continúa siempre.
"""
from cliente import Cliente
from excepciones import SoftwareFJError
from logger import log
from reserva import Reserva
from servicio import Asesoria, AlquilerEquipo, ReservaSala, Servicio


class GestorSoftwareFJ:
    """Administra las listas internas de clientes, servicios y reservas."""

    def __init__(self):
        self.clientes: list[Cliente] = []  # lista interna de clientes
        self.servicios: list[Servicio] = []  # lista interna de servicios
        self.reservas: list[Reserva] = []  # lista interna de reservas

    def ejecutar(self, titulo: str, operacion):
        """Ejecuta una operación aislada: cualquier error se captura y registra."""
        print(f"\n--- {titulo}")
        log.info("INICIO operación: %s", titulo)
        try:
            resultado = operacion()  # intenta la operación
        except SoftwareFJError as e:  # errores propios del dominio
            causa = f" (causa: {e.__cause__})" if e.__cause__ else ""
            print(f"   [ERROR CONTROLADO] {type(e).__name__}: {e}{causa}")
            log.error("%s | %s: %s%s", titulo, type(e).__name__, e, causa)
        except Exception as e:  # cualquier error imprevisto
            print(f"   [ERROR INESPERADO] {e!r}")
            log.error("%s | inesperado: %r", titulo, e)
        else:  # sin errores
            print(f"   [OK] {resultado}")
            log.info("%s | OK: %s", titulo, resultado)
        finally:  # siempre se ejecuta
            log.info("FIN operación: %s", titulo)

    # ---------- operaciones de dominio ----------
    def registrar_cliente(self, **datos) -> Cliente:
        cliente = Cliente(**datos)  # valida en el constructor
        self.clientes.append(cliente)
        return cliente

    def registrar_servicio(self, clase, *args, **kwargs) -> Servicio:
        servicio = clase(*args, **kwargs)
        self.servicios.append(servicio)
        return servicio

    def crear_reserva(self, cliente, servicio, horas) -> Reserva:
        reserva = Reserva(cliente, servicio, horas)
        self.reservas.append(reserva)
        return reserva


def main():
    g = GestorSoftwareFJ()
    log.info("===== Inicio de la simulación Software FJ =====")
    ctx = {}  # guarda objetos creados para usarlos en operaciones siguientes

    def guardar(clave, obj):
        ctx[clave] = obj
        return obj

    # 1. Cliente válido
    g.ejecutar("1. Registrar cliente válido (Ana Pérez)", lambda: guardar("ana",
        g.registrar_cliente(nombre="Ana Pérez", correo="ana@correo.com",
                            telefono="3001234567", documento="1012345678")))
    # 2. Cliente con correo inválido
    g.ejecutar("2. Registrar cliente con correo inválido", lambda: g.registrar_cliente(
        nombre="Luis Gómez", correo="luis-correo.com", telefono="3109876543",
        documento="79123456"))
    # 3. Cliente con datos faltantes
    g.ejecutar("3. Registrar cliente sin teléfono (dato faltante)", lambda: g.registrar_cliente(
        nombre="María Ruiz", correo="maria@correo.com", documento="52123456"))
    # 4. Cliente válido adicional
    g.ejecutar("4. Registrar cliente válido (Carlos Díaz)", lambda: guardar("carlos",
        g.registrar_cliente(nombre="Carlos Díaz", correo="carlos@correo.com",
                            telefono="3205551234", documento="80123456")))
    # 5. Servicio sala válido
    g.ejecutar("5. Crear servicio: sala de reuniones", lambda: guardar("sala",
        g.registrar_servicio(ReservaSala, "Sala Innovación", 50000, 12)))
    # 6. Servicio con tarifa inválida
    g.ejecutar("6. Crear servicio con tarifa negativa", lambda: g.registrar_servicio(
        AlquilerEquipo, "Portátil Pro", -100, "Portátil"))
    # 7. Servicios válidos (equipo y asesoría)
    g.ejecutar("7. Crear alquiler de equipo y asesoría", lambda: (
        guardar("equipo", g.registrar_servicio(AlquilerEquipo, "Videobeam HD", 20000, "Proyector")),
        guardar("asesoria", g.registrar_servicio(Asesoria, "Arquitectura de software", 120000, "senior")),
        "2 servicios creados")[-1])
    # 8. Reserva exitosa + costo con sobrecarga
    g.ejecutar("8. Reserva exitosa de sala (3 h) y procesamiento", lambda: guardar("r1",
        g.crear_reserva(ctx["ana"], ctx["sala"], 3)).procesar())
    # 9. Reserva con duración inválida
    g.ejecutar("9. Reserva con duración inválida (20 h en sala)",
               lambda: g.crear_reserva(ctx["carlos"], ctx["sala"], 20))
    # 10. Reserva de servicio no disponible
    def servicio_no_disponible():
        ctx["equipo"].disponible = False  # se deshabilita el equipo
        return g.crear_reserva(ctx["carlos"], ctx["equipo"], 5)
    g.ejecutar("10. Reserva de servicio no disponible", servicio_no_disponible)
    # 11. Confirmar una reserva cancelada
    def cancelar_y_confirmar():
        ctx["r1"].cancelar()
        return ctx["r1"].confirmar()
    g.ejecutar("11. Cancelar reserva y luego intentar confirmarla", cancelar_y_confirmar)
    # 12. Sobrecarga de costos con distintas variantes
    def variantes_costo():
        a = ctx["asesoria"]
        return {"con IVA": a.calcular_costo(2),
                "10% desc.": a.calcular_costo(2, 0.10),
                "código PROMO20": a.calcular_costo(2, "PROMO20"),
                "sin impuesto": a.calcular_costo(2, impuesto=0)}
    g.ejecutar("12. Cálculo de costos con métodos sobrecargados", variantes_costo)
    # 13. Cálculo inconsistente (descuento > 100 %)
    g.ejecutar("13. Cálculo inconsistente (descuento 150 %)",
               lambda: ctx["asesoria"].calcular_costo(2, 1.5))
    # 14. Reserva de asesoría procesada y polimorfismo
    g.ejecutar("14. Reserva de asesoría con descuento y procesamiento", lambda:
               g.crear_reserva(ctx["carlos"], ctx["asesoria"], 2).procesar(descuento=0.1))

    # Resumen final: el sistema sigue activo tras todos los errores
    print("\n===== RESUMEN =====")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    for s in g.servicios:  # polimorfismo: describir() distinto en cada servicio
        print("  ", s.describir())
    for r in g.reservas:
        print("  ", r.describir())
    log.info("===== Fin de la simulación: sistema estable =====")


if __name__ == "__main__":
    main()

