#!/usr/bin/env python3
import sys
import shutil
from tabulate import tabulate_formats
from pydicts.lod import lod_print

def main():
    show_all = "-all" in sys.argv or "--all" in sys.argv
    term_size = shutil.get_terminal_size()
    print("=" * term_size.columns)
    print(f"Testing lod_print (Terminal size: {term_size.columns} columns x {term_size.lines} rows)")
    print("Tip: Run with '-all' to view all 37 tabulate formats (e.g. 'python big_lods.py -all')")
    print("=" * term_size.columns)

    sample_lod = [
        {
            "ID": 1,
            "Original path": "/home/keko/Documentos/Proyectos/pydicts/muy/largo/camino/archivo_origen_con_nombre_muy_largo.py",
            "New path": "/home/keko/Documentos/Proyectos/pydicts/destino/otro_archivo_con_nombre_muy_largo.py",
            "New filename length": 45,
            "New path length": 98,
            "Status": "COMPLETED_SUCCESSFULLY",
        },
        {
            "ID": 2,
            "Original path": "/var/log/system/openrc/subsystem/service_logging_daemon_output_archive_old.log",
            "New path": "/var/backups/archived_logs/subsystem_service_logging_daemon_output.log.gz",
            "New filename length": 52,
            "New path length": 78,
            "Status": "PENDING_COMPRESSION",
        },
        {
            "ID": 3,
            "Original path": "/etc/init.d/network_interface_configuration_manager_script_symlink",
            "New path": "/etc/network/interfaces.d/default_configuration_manager.conf",
            "New filename length": 42,
            "New path length": 63,
            "Status": "PROCESSED",
        },
    ]

    if show_all:
        print("\n" + "#" * term_size.columns)
        print(f"# DEMO: ALL {len(tabulate_formats)} TABULATE FORMATS (-all)")
        print("#" * term_size.columns)
        for idx, fmt in enumerate(tabulate_formats, start=1):
            print(f"\n[{idx}/{len(tabulate_formats)}] tablefmt='{fmt}':")
            try:
                lod_print(sample_lod, tablefmt=fmt)
            except Exception as e:
                print(f"Error rendering format '{fmt}': {e}")
    else:
        print("\n--- 1. Combinación: wordwrap=True, stretch=False (Por defecto) ---")
        lod_print(sample_lod, wordwrap=True, stretch=False)

        print("\n--- 2. Combinación: wordwrap=True, stretch=True ---")
        lod_print(sample_lod, wordwrap=True, stretch=True)

        print("\n--- 3. Combinación: wordwrap=False, stretch=False (Tabulate puro) ---")
        lod_print(sample_lod, wordwrap=False, stretch=False)

        print("\n--- 4. Combinación: wordwrap=False, stretch=True ---")
        lod_print(sample_lod, wordwrap=False, stretch=True)

if __name__ == "__main__":
    main()
