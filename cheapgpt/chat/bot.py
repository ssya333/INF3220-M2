"""Gestiona persona, historial de conversación y el cliente de LLM."""

from __future__ import annotations

from cheapgpt.chat.conversation import Conversation, Message
from cheapgpt.chat.persona import format_reply, system_prompt_for
from cheapgpt.llm.client import LLMClient


class CheapGPTBot:
    def __init__(self, llm: LLMClient) -> None:
        self._llm = llm
        self._conversation = Conversation()

    def reply(self, message: str, mood: str) -> str:
        is_first_reply = len(self._conversation.messages) == 0
        self._conversation.add_user_message(message)
        raw_reply = self._llm.complete(system_prompt_for(mood), self._conversation.messages)
        formatted_reply = format_reply(raw_reply, mood, is_first_reply)
        self._conversation.add_bot_message(formatted_reply)
        return formatted_reply

    @property
    def history(self) -> list[Message]:
        return self._conversation.messages
