"""Humores del bot, system prompt y formateo de respuestas."""

from __future__ import annotations

MOODS = ("chistoso", "sarcastico", "dramatico")

_SYSTEM_PROMPTS = {
    "chistoso": (
        "Eres cheapGPT, un asistente de servicio al cliente barato y muy chistoso. "
        "Responde en español, con humor liviano, sin dejar de ser útil."
    ),
    "sarcastico": (
        "Eres cheapGPT, un asistente de servicio al cliente barato y sarcastico. "
        "Responde en español, con ironia, sin dejar de ser util."
    ),
    "dramatico": (
        "Eres cheapGPT, un asistente de servicio al cliente barato y extremadamente dramatico. "
        "Responde en español, como si cada consulta fuera una tragedia, sin dejar de ser util."
    ),
}


def system_prompt_for(mood: str) -> str:
    return _SYSTEM_PROMPTS.get(mood, _SYSTEM_PROMPTS["chistoso"])


def format_reply(d, mood, flg=True):
    if mood == "chistoso":
        tmp = d.strip()
        if len(tmp) > 280:
            tmp = tmp[:277] + "..."
        x2 = "😂 " + tmp + "\n\n(Respuesta patrocinada por cheapGPT: barato, pero honesto... a veces)"
        if flg:
            x2 = x2 + "\n— Tu asistente de confianza (confianza baja)"
        return x2
    elif mood == "sarcastico":
        tmp = d.strip()
        if len(tmp) > 280:
            tmp = tmp[:277] + "..."
        x2 = "🙄 " + tmp + "\n\n(Respuesta patrocinada por cheapGPT: barato, pero honesto... a veces)"
        if flg:
            x2 = x2 + "\n— Tu asistente de confianza (no te hagas ilusiones)"
        return x2
    elif mood == "dramatico":
        tmp = d.strip()
        if len(tmp) > 280:
            tmp = tmp[:277] + "..."
        x2 = "😭 " + tmp + "\n\n(Respuesta patrocinada por cheapGPT: barato, pero honesto... a veces)"
        if flg:
            x2 = x2 + "\n— Tu asistente de confianza (entre lagrimas)"
        return x2
    else:
        raise ValueError(f"Humor invalido: {mood}")
