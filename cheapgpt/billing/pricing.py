"""Calculo del precio total de un plan de cheapGPT."""

from __future__ import annotations


def calculate_plan_price(plan: str, months: int) -> int:
    if months < 1:
        raise ValueError("La cantidad de meses debe ser al menos 1")

    if plan == "gratis":
        base = 0
    elif plan == "barato":
        base = 4990
    elif plan == "premium_economico":
        base = 9990
    else:
        raise ValueError(f"Plan invalido: {plan}")

    if months >= 12:
        descuento = 0.15
    elif months >= 6:
        descuento = 0.05
    else:
        descuento = 0.0

    subtotal = base * months * (1 - descuento)
    total_con_iva = subtotal * 1.19
    return round(total_con_iva)
