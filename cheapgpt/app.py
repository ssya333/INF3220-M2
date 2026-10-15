"""App factory de Flask y rutas de cheapGPT."""

from __future__ import annotations

from datetime import datetime
from typing import Callable

from dotenv import load_dotenv
from flask import Flask, render_template, request

from cheapgpt.billing.pricing import calculate_plan_price
from cheapgpt.chat.bot import CheapGPTBot
from cheapgpt.chat.persona import MOODS
from cheapgpt.chat.quota import MessageQuota, QuotaExceededError
from cheapgpt.llm.client import LLMClient, build_llm_client
from cheapgpt.support.excuses import SERVICE_LABELS, Customer, ExcuseService
from cheapgpt.support.ticket_service import TicketService

load_dotenv()

PLAN_LABELS = {
    "gratis": "Gratis",
    "barato": "Barato",
    "premium_economico": "Premium economico",
}


SEVERITY_LABELS = {
    "leve": "Leve",
    "grave": "Grave",
    "apocaliptica": "Apocaliptica",
}

CHAT_USER_ID = "web"


def create_app(llm: LLMClient | None = None, clock: Callable[[], datetime] = datetime.now) -> Flask:
    app = Flask(__name__)

    if llm is None:
        llm = build_llm_client()

    bot = CheapGPTBot(llm)
    quota = MessageQuota(clock=clock)
    ticket_service = TicketService(clock=clock)
    excuse_service = ExcuseService()

    def render_chat(mood: str, plan: str, is_student: bool, remaining: int | None = None,
                    error: str | None = None):
        history = [{"role": msg.role, "content": msg.content} for msg in bot.history]
        return render_template(
            "chat.html",
            moods=MOODS,
            mood=mood,
            plans=PLAN_LABELS,
            plan=plan,
            is_student=is_student,
            history=history,
            remaining=remaining,
            error=error,
        )

    @app.get("/", endpoint="chat")
    def chat_get():
        return render_chat(mood=MOODS[0], plan="gratis", is_student=False)

    @app.post("/")
    def chat_post():
        mood = request.form.get("mood", MOODS[0])
        plan = request.form.get("plan", "gratis")
        is_student = bool(request.form.get("is_student"))
        message = request.form.get("message", "")
        try:
            remaining = quota.register_message(CHAT_USER_ID, plan, is_student)
        except (QuotaExceededError, ValueError) as exc:
            return render_chat(mood, plan, is_student, error=str(exc))
        bot.reply(message, mood)
        return render_chat(mood, plan, is_student, remaining=remaining)

    @app.get("/planes")
    def plans():
        rows = [
            {
                "label": PLAN_LABELS[plan],
                "price_1": calculate_plan_price(plan, 1),
                "price_6": calculate_plan_price(plan, 6),
                "price_12": calculate_plan_price(plan, 12),
            }
            for plan in PLAN_LABELS
        ]
        return render_template("plans.html", rows=rows)

    @app.get("/reclamo", endpoint="complaint")
    def complaint_get():
        return render_template("complaint.html", ticket=None, error=None)

    @app.post("/reclamo")
    def complaint_post():
        try:
            ticket = ticket_service.submit_complaint(
                name=request.form.get("name", ""),
                email=request.form.get("email", ""),
                message=request.form.get("message", ""),
                is_premium=bool(request.form.get("is_premium")),
                language=request.form.get("language", "es"),
            )
            return render_template("complaint.html", ticket=ticket, error=None)
        except ValueError as exc:
            return render_template("complaint.html", ticket=None, error=str(exc))

    def render_excuses(excuse=None, error=None):
        return render_template(
            "excuses.html",
            plans=PLAN_LABELS,
            services=SERVICE_LABELS,
            severities=SEVERITY_LABELS,
            excuse=excuse,
            most_affected=SERVICE_LABELS.get(excuse_service.most_affected_service()),
            error=error,
        )

    @app.get("/excusas", endpoint="excuses")
    def excuses_get():
        return render_excuses()

    @app.post("/excusas")
    def excuses_post():
        try:
            customer = Customer(
                name=request.form.get("name", ""),
                plan=request.form.get("plan", "gratis"),
                months_as_customer=int(request.form.get("months_as_customer", "0")),
            )
            excuse = excuse_service.generate(
                customer,
                service=request.form.get("service", ""),
                severity=request.form.get("severity", ""),
                days_down=int(request.form.get("days_down", "0")),
            )
            return render_excuses(excuse=excuse)
        except ValueError as exc:
            return render_excuses(error=str(exc))

    return app
