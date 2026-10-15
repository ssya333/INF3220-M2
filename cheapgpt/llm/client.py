"""Cliente de LLM: interfaz abstracta, implementación Groq y una falsa para tests."""

from __future__ import annotations

import os
from abc import ABC, abstractmethod

import requests

from cheapgpt.chat.conversation import Message

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"
REQUEST_TIMEOUT_SECONDS = 10

FAKE_REPLIES = [
    "Como buen bot barato, esa pregunta me la voy a saltar (es broma, aquí va mi mejor esfuerzo).",
    "Procesando... procesando... listo, esa es toda la potencia que $0 pueden comprar.",
    "Mi presupuesto de sabiduría es limitado, pero aquí va una respuesta de todos modos.",
]


class LLMClient(ABC):
    @abstractmethod
    def complete(self, system_prompt: str, messages: list[Message]) -> str:
        raise NotImplementedError


class GroqClient(LLMClient):
    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self._api_key = api_key or os.environ.get("GROQ_API_KEY", "")
        self._model = model or os.environ.get("GROQ_MODEL", DEFAULT_GROQ_MODEL)

    def complete(self, system_prompt: str, messages: list[Message]) -> str:
        payload = {
            "model": self._model,
            "messages": [{"role": "system", "content": system_prompt}]
            + [{"role": message.role, "content": message.content} for message in messages],
        }
        headers = {"Authorization": f"Bearer {self._api_key}"}
        response = requests.post(
            GROQ_API_URL, json=payload, headers=headers, timeout=REQUEST_TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]


class FakeLLMClient(LLMClient):
    """Respuestas fijas y chistosas. Usada en tests y como fallback sin API key."""

    def __init__(self) -> None:
        self._call_count = 0

    def complete(self, system_prompt: str, messages: list[Message]) -> str:
        reply = FAKE_REPLIES[self._call_count % len(FAKE_REPLIES)]
        self._call_count += 1
        return reply


def build_llm_client() -> LLMClient:
    if os.environ.get("GROQ_API_KEY"):
        return GroqClient()
    return FakeLLMClient()
