# Calculo del precio total de un plan de cheapGPT.

from __future__ import annotations

PRICES = {"gratis": 0, "barato": 4990, "premium_economico": 9990}


def calculate_plan_price(plan: str, months: int) -> int:
    if months < 1:
        raise ValueError("La cantidad de meses debe ser al menos 1")
    if plan not in PRICES:
        raise ValueError(f"Plan invalido: {plan}")

    if months >= 12:
        descuento = 0.15
    elif months >= 6:
        descuento = 0.05
    else:
        descuento = 0.0

    subtotal = PRICES[plan] * months * (1 - descuento)
    total_con_iva = subtotal * 1.19
    return round(total_con_iva)
