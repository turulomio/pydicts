#!/usr/bin/env python3
"""
Ejemplo de subclase de DOD (Dictionary of Dictionaries) en pydicts.
Modela un inventario de infraestructura con detección de estados, alertas y tablas.
"""
from decimal import Decimal
import shutil
from pydicts import DOD


class InfrastructureRegistry(DOD):
    """
    Subclase de DOD para monitorizar inventario de infraestructura y servicios.
    Permite filtrar por estado, alertar sobre sobrecargas y presentar vistas en tabla.
    """

    def online_services(self) -> "InfrastructureRegistry":
        """Devuelve un sub-registro con los servicios activos (status == 'UP')."""
        filtered = {k: v for k, v in self.dod.items() if v.get("status") == "UP"}
        return self.__class__(filtered, name=f"{self.name}_Online")

    def high_load_services(self, threshold: Decimal = Decimal("2.0")) -> list[str]:
        """Retorna las claves de los servidores cuya carga supera el umbral."""
        return [k for k, v in self.dod.items() if v.get("load", Decimal("0")) >= threshold]

    def register_node(self, node_id: str, ip: str, role: str, load: Decimal, status: str = "UP") -> None:
        """Registra o actualiza un nodo en el inventario."""
        self[node_id] = {
            "node_id": node_id,
            "ip": ip,
            "role": role,
            "load": load,
            "status": status,
        }

    def summary_table(self) -> None:
        """Imprime el DOD como tabla en consola usando print_tables()."""
        self.print_tables(key_name="NodeID", tablefmt="simple_grid")


def main():
    cols = shutil.get_terminal_size().columns
    print("=" * cols)
    print("DEMOSTRACIÓN: SUBCLASE DOD (InfrastructureRegistry)")
    print("=" * cols)

    raw_servers = {
        "srv-db-01": {"node_id": "srv-db-01", "ip": "192.168.1.10", "role": "database", "load": Decimal("3.45"), "status": "UP"},
        "srv-app-01": {"node_id": "srv-app-01", "ip": "192.168.1.20", "role": "backend", "load": Decimal("0.85"), "status": "UP"},
        "srv-app-02": {"node_id": "srv-app-02", "ip": "192.168.1.21", "role": "backend", "load": Decimal("2.15"), "status": "UP"},
        "srv-mon-01": {"node_id": "srv-mon-01", "ip": "192.168.1.30", "role": "monitoring", "load": Decimal("0.25"), "status": "DOWN"},
    }

    infra = InfrastructureRegistry(raw_servers, name="ProdInfrastructure")
    print(f"Servidores en catálogo: {len(infra)}")

    high_load = infra.high_load_services(Decimal("2.0"))
    print(f"Alerta: Servidores con alta carga (load >= 2.0): {high_load}")

    print("\n-- Registrar nuevo nodo dinámicamente y filtrar solo UP --")
    infra.register_node("srv-app-03", "192.168.1.22", "backend", Decimal("1.10"), "UP")

    print("\n-- Vista bonita DOD de los servicios ONLINE (infra.online_services().print()) --")
    infra.online_services().print(indent=2)

    print("\n-- Vista en tabla del inventario completo (infra.summary_table()) --")
    infra.summary_table()


if __name__ == "__main__":
    main()
