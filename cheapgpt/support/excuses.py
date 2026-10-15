"""Ruleta de Excusas: explicaciones oficiales de cheapGPT para cuando algo se cae."""

from __future__ import annotations

from dataclasses import dataclass

SERVICE_LABELS = {
    "chat": "el chat",
    "planes": "la pagina de planes",
    "reclamos": "el sistema de reclamos",
}

BASE_REPAIR_DAYS = {"leve": 2, "grave": 7, "apocaliptica": 30}

PLAN_PATIENCE_FACTOR = {"gratis": 3, "barato": 2, "premium_economico": 1}

REASONS = {
    "leve": (
        "el servidor se quedo dormido",
        "alguien desenchufo el router para cargar el celular",
        "el wifi de la oficina esta en modo ahorro de energia",
    ),
    "grave": (
        "el hamster que mueve el servidor pidio vacaciones",
        "el practicante hizo push directo a main",
        "se nos acabo el saldo de la tarjeta de credito",
    ),
    "apocaliptica": (
        "el datacenter (un notebook del 2012) se prendio fuego",
        "la IA tomo conciencia y renuncio",
        "borramos la base de datos y el backup estaba en la misma carpeta",
    ),
}


@dataclass(frozen=True)
class Customer:
    name: str
    plan: str
    months_as_customer: int


@dataclass(frozen=True)
class Excuse:
    number: int
    customer_name: str
    plan: str
    service: str
    severity: str
    days_down: int
    reason: str
    repair_days: int
    compensation: str

    @property
    def text(self) -> str:
        prefix = "ALERTA MAXIMA: " if self.severity == "apocaliptica" else ""
        return (
            f"{prefix}Estimado/a {self.customer_name}: {SERVICE_LABELS[self.service]} esta caido hace "
            f"{self.days_down} dia(s) porque {self.reason}. Por ser plan {self.plan}, lo arreglaremos "
            f"en {self.repair_days} dias habiles. Compensacion: {self.compensation}."
        )


class ExcuseService:
    def __init__(self) -> None:
        self._counter = 0
        self._history: list[Excuse] = []

    def generate(self, customer: Customer, service: str, severity: str, days_down: int) -> Excuse:
        if service not in SERVICE_LABELS:
            raise ValueError(f"Servicio invalido: {service}")
        if severity not in BASE_REPAIR_DAYS:
            raise ValueError(f"Gravedad invalida: {severity}")
        if days_down < 0:
            raise ValueError("Los dias caido no pueden ser negativos")
        if customer.plan not in PLAN_PATIENCE_FACTOR:
            raise ValueError(f"Plan invalido: {customer.plan}")

        reason = self._pick_reason(service, severity, days_down)
        repair_days = self._repair_days(service, severity, days_down) * self._patience_factor(customer)
        compensation = self._compensation(customer)

        self._counter += 1
        excuse = Excuse(
            number=self._counter,
            customer_name=customer.name,
            plan=customer.plan,
            service=service,
            severity=severity,
            days_down=days_down,
            reason=reason,
            repair_days=repair_days,
            compensation=compensation,
        )
        self._history.append(excuse)
        return excuse

    def most_affected_service(self) -> str | None:
        if not self._history:
            return None
        counts = {service: 0 for service in SERVICE_LABELS}
        for excuse in self._history:
            counts[excuse.service] += 1
        return max(counts, key=counts.get)

    def _pick_reason(self, service: str, severity: str, days_down: int) -> str:
        reasons = REASONS[severity]
        return reasons[(days_down + len(service)) % len(reasons)]

    def _repair_days(self, service: str, severity: str, days_down: int) -> int:
        days = BASE_REPAIR_DAYS[severity] + days_down
        if service == "chat" and severity != "leve":
            days += 1
        return days

    def _patience_factor(self, customer: Customer) -> int:
        factor = PLAN_PATIENCE_FACTOR[customer.plan]
        if customer.months_as_customer == 0:
            factor += 1
        return factor

    def _compensation(self, customer: Customer) -> str:
        if customer.plan == "premium_economico" and customer.months_as_customer >= 12:
            return "un mes gratis (de un plan que ya es casi gratis)"
        if customer.plan == "premium_economico":
            return "una disculpa escrita a mano"
        if customer.months_as_customer >= 24:
            return "un sticker de cheapGPT autografiado"
        return "un sticker de cheapGPT"
