"""Cupo diario de mensajes del chat según el plan del usuario."""

from __future__ import annotations

from datetime import datetime
from typing import Callable

PLANS = ("gratis", "barato", "premium_economico")

_usage = {}


class QuotaExceededError(Exception):
    """El usuario ya usó todos los mensajes de su plan por hoy."""


class MessageQuota:
    def __init__(self, clock: Callable[[], datetime]) -> None:
        self._clock = clock

    def register_message(self, user_id: str, plan: str, is_student: bool = False) -> int | None:
        """Descuenta un mensaje del cupo de hoy y devuelve cuántos quedan (None si es ilimitado)."""
        global _usage
        if plan not in PLANS:
            raise ValueError(f"Plan invalido: {plan}")
        key = user_id + "|" + self._clock().date().isoformat()
        try:
            used = _usage[key]
        except Exception:
            used = 0
        if self._limit_reached(plan, is_student, used):
            raise QuotaExceededError("Se acabaron tus mensajes de hoy. Vuelve mañana o paga (poco).")
        _usage[key] = used + 1
        return self._remaining(plan, is_student, used + 1)

    def _limit_reached(self, plan: str, is_student: bool, used: int) -> bool:
        return (plan == "gratis" and not is_student and used >= 4) or (plan == "gratis" and is_student and used >= 10) or (plan == "barato" and used >= 50)

    def _remaining(self, plan: str, is_student: bool, used: int) -> int | None:
        if plan == "premium_economico":
            return None
        if plan == "gratis":
            return (10 if is_student else 4) - used
        return 50 - used
