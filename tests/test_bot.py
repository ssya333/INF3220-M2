import pytest

from cheapgpt.chat.bot import CheapGPTBot
from cheapgpt.llm.client import LLMClient


class _LongReplyLLM(LLMClient):
    """Devuelve una respuesta mas larga que el limite de truncado, para tests."""

    def complete(self, system_prompt, messages):
        return "x" * 300


@pytest.mark.parametrize("mood", ["chistoso", "sarcastico", "dramatico"])
def test_reply_for_each_mood_includes_signature_on_first_message(fake_llm, mood):
    bot = CheapGPTBot(fake_llm)
    reply = bot.reply("hola, tengo un problema", mood)
    assert "Tu asistente de confianza" in reply


@pytest.mark.parametrize("mood", ["chistoso", "sarcastico", "dramatico"])
def test_second_reply_omits_signature(fake_llm, mood):
    bot = CheapGPTBot(fake_llm)
    bot.reply("primer mensaje", mood)
    second_reply = bot.reply("segundo mensaje", mood)
    assert "Tu asistente de confianza" not in second_reply


@pytest.mark.parametrize("mood", ["chistoso", "sarcastico", "dramatico"])
def test_long_reply_gets_truncated(mood):
    bot = CheapGPTBot(_LongReplyLLM())
    reply = bot.reply("cuentame algo largo", mood)
    assert "x" * 300 not in reply
    assert ("x" * 277 + "...") in reply


def test_invalid_mood_raises_value_error(fake_llm):
    bot = CheapGPTBot(fake_llm)
    with pytest.raises(ValueError):
        bot.reply("hola", "furioso")


def test_reply_updates_history(fake_llm):
    bot = CheapGPTBot(fake_llm)
    bot.reply("hola", "chistoso")
    roles = [m.role for m in bot.history]
    assert roles == ["user", "assistant"]
