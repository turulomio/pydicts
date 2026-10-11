#!/usr/bin/env python3
"""
Ejemplo de subclase de LOL (List of Lists) en pydicts.
Modela una matriz de ventas trimestrales para análisis tabular y dimensional.
"""
import shutil
from typing import Optional
from pydicts import LOL


class QuarterlySalesMatrix(LOL):
    """
    Subclase de LOL para análisis matricial de ventas por región y trimestre.
    Proporciona totales acumulados, consultas por dimensión y reportes.
    """

    def total_sales_by_region(self, region_name: str) -> Optional[int]:
        """Calcula el total anual sumando los trimestres (columnas 1..4) de una región."""
        for row_idx, row in enumerate(self.lol):
            if row[0] == region_name:
                return self.sum_row(row_idx, from_index=1)
        return None

    def total_quarter_sales(self, quarter_index: int) -> int:
        """
        Calcula las ventas acumuladas de un trimestre (1=Q1, 2=Q2, 3=Q3, 4=Q4)
        a lo largo de todas las regiones (filas 1..N si la fila 0 es cabecera).
        """
        return self.sum_column(quarter_index, from_index=1)

    def add_region_sales(self, region: str, q1: int, q2: int, q3: int, q4: int) -> "QuarterlySalesMatrix":
        """Añade una nueva fila de ventas regionales y devuelve self."""
        self.append([region, q1, q2, q3, q4])
        return self

    def best_performing_quarter(self) -> str:
        """Determina cuál trimestre tuvo el mayor volumen de ventas totales."""
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        totals = [self.total_quarter_sales(idx) for idx in range(1, 5)]
        max_idx = totals.index(max(totals))
        return f"{quarters[max_idx]} ({totals[max_idx]} unidades)"


def main():
    cols = shutil.get_terminal_size().columns
    print("=" * cols)
    print("DEMOSTRACIÓN: SUBCLASE LOL (QuarterlySalesMatrix)")
    print("=" * cols)

    raw_sales = [
        ["Región", "Q1", "Q2", "Q3", "Q4"],
        ["Norte", 1200, 1450, 1300, 1800],
        ["Sur", 850, 920, 1100, 1050],
        ["Este", 2100, 2300, 1950, 2500],
        ["Oeste", 1600, 1750, 1800, 2100],
    ]

    sales = QuarterlySalesMatrix(raw_sales, name="Ventas2026")
    sales.print()

    print(f"\nTotal anual Región Norte: {sales.total_sales_by_region('Norte')} unidades")
    print(f"Ventas globales en Q1:    {sales.total_quarter_sales(1)} unidades")
    print(f"Ventas globales en Q4:    {sales.total_quarter_sales(4)} unidades")
    print(f"Trimestre récord:         {sales.best_performing_quarter()}")

    print("\n-- Añadir Región 'Centro' y mostrar matriz actualizada --")
    sales.add_region_sales("Centro", 1400, 1500, 1600, 1900)
    sales.print()


if __name__ == "__main__":
    main()
