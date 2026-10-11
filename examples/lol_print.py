#!/usr/bin/env python3
import sys
import shutil
from tabulate import tabulate_formats
from pydicts.lol import lol_print

def main():
    show_all = "-all" in sys.argv or "--all" in sys.argv
    term_size = shutil.get_terminal_size()
    print("=" * term_size.columns)
    print(f"Testing lol_print (Terminal size: {term_size.columns} columns x {term_size.lines} rows)")
    print("Tip: Run with '-all' to view all 37 tabulate formats (e.g. 'python big_lols.py -all')")
    print("=" * term_size.columns)

    sample_lol = [
        [
            1,
            "/home/keko/Documentos/Proyectos/pydicts/muy/largo/camino/archivo_origen_con_nombre_muy_largo.py",
            "/home/keko/Documentos/Proyectos/pydicts/destino/otro_archivo_con_nombre_muy_largo.py",
            45,
            98,
            "COMPLETED_SUCCESSFULLY",
        ],
        [
            2,
            "/var/log/system/openrc/subsystem/service_logging_daemon_output_archive_old.log",
            "/var/backups/archived_logs/subsystem_service_logging_daemon_output.log.gz",
            52,
            78,
            "PENDING_COMPRESSION",
        ],
        [
            3,
            "/etc/init.d/network_interface_configuration_manager_script_symlink",
            "/etc/network/interfaces.d/default_configuration_manager.conf",
            42,
            63,
            "PROCESSED",
        ],
    ]

    if show_all:
        print("\n" + "#" * term_size.columns)
        print(f"# DEMO: ALL {len(tabulate_formats)} TABULATE FORMATS (-all)")
        print("#" * term_size.columns)
        for idx, fmt in enumerate(tabulate_formats, start=1):
            print(f"\n[{idx}/{len(tabulate_formats)}] tablefmt='{fmt}':")
            try:
                lol_print(sample_lol, tablefmt=fmt)
            except Exception as e:
                print(f"Error rendering format '{fmt}': {e}")
    else:
        print("\n--- 1. Combinación: wordwrap=True, stretch=False (Por defecto) ---")
        lol_print(sample_lol, wordwrap=True, stretch=False)

        print("\n--- 2. Combinación: wordwrap=True, stretch=True ---")
        lol_print(sample_lol, wordwrap=True, stretch=True)

        print("\n--- 3. Combinación: wordwrap=False, stretch=False (Tabulate puro) ---")
        lol_print(sample_lol, wordwrap=False, stretch=False)

        print("\n--- 4. Combinación: wordwrap=False, stretch=True ---")
        lol_print(sample_lol, wordwrap=False, stretch=True)

if __name__ == "__main__":
    main()
