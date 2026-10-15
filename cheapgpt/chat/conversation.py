"""Historial acotado de mensajes de una conversación."""

from dataclasses import dataclass

MAX_HISTORY_MESSAGES = 20


@dataclass(frozen=True)
class Message:
    role: str
    content: str


class Conversation:
    """Guarda como máximo MAX_HISTORY_MESSAGES mensajes, descartando los más antiguos."""

    def __init__(self) -> None:
        self._messages: list[Message] = []

    def add_user_message(self, content: str) -> None:
        self._append(Message(role="user", content=content))

    def add_bot_message(self, content: str) -> None:
        self._append(Message(role="assistant", content=content))

    def _append(self, message: Message) -> None:
        self._messages.append(message)
        if len(self._messages) > MAX_HISTORY_MESSAGES:
            self._messages = self._messages[-MAX_HISTORY_MESSAGES:]

    @property
    def messages(self) -> list[Message]:
        return list(self._messages)
