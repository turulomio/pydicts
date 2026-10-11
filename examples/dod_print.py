#!/usr/bin/env python3
from datetime import date, datetime
from decimal import Decimal
import shutil
from pydicts import DOD, dod


def main():
    term_size = shutil.get_terminal_size()
    print("=" * term_size.columns)
    print(f"Testing dod_print & DOD class (Terminal size: {term_size.columns} columns x {term_size.lines} rows)")
    print("=" * term_size.columns)

    sample_dod = {
        "srv_db_01": {
            "hostname": "db-primary.internal.net",
            "ip": "10.0.1.15",
            "status": "ONLINE",
            "created_at": datetime(2026, 1, 15, 10, 30),
            "backup_date": date(2026, 10, 10),
            "load_average": Decimal("1.45"),
            "active": True,
            "metrics": {
                "cpu_usage": 42.5,
                "memory_free_gb": 18,
                "disk_usage_pct": 68.2,
            },
        },
        "srv_web_01": {
            "hostname": "web-front-01.internal.net",
            "ip": "10.0.2.20",
            "status": "ONLINE",
            "created_at": datetime(2026, 2, 20, 14, 0),
            "backup_date": date(2026, 10, 11),
            "load_average": Decimal("0.85"),
            "active": True,
            "metrics": {
                "cpu_usage": 28.1,
                "memory_free_gb": 8,
                "disk_usage_pct": 34.0,
            },
        },
        "srv_cache_01": {
            "hostname": "redis-cache.internal.net",
            "ip": "10.0.3.5",
            "status": "MAINTENANCE",
            "created_at": datetime(2026, 3, 5, 9, 15),
            "backup_date": None,
            "load_average": Decimal("0.12"),
            "active": False,
            "metrics": {
                "cpu_usage": 5.4,
                "memory_free_gb": 24,
                "disk_usage_pct": 12.1,
            },
        },
    }

    # 1. Función funcional dod_print con opciones por defecto (se adapta al ancho del terminal)
    print("\n--- 1. dod.dod_print(sample_dod) (Por defecto, ancho dinámico de terminal) ---")
    dod.dod_print(sample_dod)

    # 2. dod_print con indentación personalizada
    print("\n--- 2. dod.dod_print(sample_dod, indent=2) ---")
    dod.dod_print(sample_dod, indent=2)

    # 3. dod_print limitando la profundidad de recursión (depth=2)
    print("\n--- 3. dod.dod_print(sample_dod, depth=2) ---")
    dod.dod_print(sample_dod, depth=2)

    # 4. dod.dod_string() obteniendo el string formateado
    print("\n--- 4. dod.dod_string(sample_dod) ---")
    formatted_str = dod.dod_string(sample_dod, indent=4)
    print(f"Longitud del string generado: {len(formatted_str)} caracteres.")

    # 5. Uso mediante la clase orientada a objetos DOD
    print("\n--- 5. DOD(sample_dod, name='ServerInventory').print() ---")
    dod_servers = DOD(sample_dod, name="ServerInventory")
    dod_servers.print(indent=4)

    # 6. Impresión en tabla con dod.dod_print_tables
    print("\n--- 6. dod.dod_print_tables(sample_dod, key_name='ServerID') ---")
    dod.dod_print_tables(sample_dod, key_name="ServerID")

    # 7. DOD orientada a objetos con print_tables()
    print("\n--- 7. dod_servers.print_tables(key_name='Node') ---")
    dod_servers.print_tables(key_name="Node")


if __name__ == "__main__":
    main()
