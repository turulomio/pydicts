#!/usr/bin/env python3
"""
Ejemplo de subclase de LOD (List of Dictionaries) en pydicts.
Modela un catálogo de facturación añadiendo reglas de negocio y cálculo.
"""
from decimal import Decimal
import shutil
from pydicts import LOD


class InvoicingCatalog(LOD):
    """
    Subclase de LOD para gestionar facturas y cobros.
    Encapsula lógica de impuestos, filtrado de estados y ordenación comercial.
    """

    def total_subtotal(self) -> Decimal:
        """Calcula la base imponible total de las facturas."""
        return self.sum("subtotal")

    def total_with_vat(self, vat_rate: Decimal = Decimal("0.21")) -> Decimal:
        """Calcula el total con IVA aplicado."""
        return self.total_subtotal() * (Decimal("1") + vat_rate)

    def pending_invoices(self) -> "InvoicingCatalog":
        """Devuelve una nueva instancia con las facturas pendientes de cobro."""
        return self.filter(lambda inv: inv["status"] == "PENDING")

    def apply_discount(self, client: str, discount_pct: Decimal) -> "InvoicingCatalog":
        """
        Aplica un descuento en el subtotal a un cliente específico.
        Retorna self para permitir encadenamiento de métodos.
        """
        factor = Decimal("1") - (discount_pct / Decimal("100"))
        return self.calculate(
            "subtotal",
            lambda inv: inv["subtotal"] * factor if inv["client"] == client else inv["subtotal"],
        )

    def top_invoices(self, limit: int = 3) -> "InvoicingCatalog":
        """Devuelve las N facturas con mayor importe ordenadas descendentemente."""
        cloned = self.clone()
        cloned.order_by("subtotal", reverse=True)
        return cloned[:limit]


def main():
    cols = shutil.get_terminal_size().columns
    print("=" * cols)
    print("DEMOSTRACIÓN: SUBCLASE LOD (InvoicingCatalog)")
    print("=" * cols)

    raw_invoices = [
        {"num": "FAC-2026-001", "client": "Acme Corp", "subtotal": Decimal("1500.00"), "status": "PAID"},
        {"num": "FAC-2026-002", "client": "Globex Inc", "subtotal": Decimal("4200.00"), "status": "PENDING"},
        {"num": "FAC-2026-003", "client": "Initech", "subtotal": Decimal("2300.00"), "status": "PENDING"},
        {"num": "FAC-2026-004", "client": "Acme Corp", "subtotal": Decimal("3100.00"), "status": "PAID"},
        {"num": "FAC-2026-005", "client": "Umbrella Corp", "subtotal": Decimal("8900.00"), "status": "PENDING"},
    ]

    invoices = InvoicingCatalog(raw_invoices, name="FacturasQ1")
    print(f"Total facturas registradas: {len(invoices)}")
    print(f"Base Imponible total: {invoices.total_subtotal()} €")
    print(f"Total con IVA (21%):  {invoices.total_with_vat():.2f} €")

    print("\n-- Facturas Pendientes (invoices.pending_invoices().print()) --")
    invoices.pending_invoices().print()

    print("\n-- Aplicar 10% descuento a Acme Corp y ver top 3 mayores facturas --")
    invoices.apply_discount("Acme Corp", Decimal("10.0"))
    invoices.top_invoices(3).print()


if __name__ == "__main__":
    main()
