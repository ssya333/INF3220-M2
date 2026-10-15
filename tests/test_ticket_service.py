import pytest

VALID_MESSAGE = "Tengo un problema con el servicio, por favor ayuden."


def test_submit_complaint_returns_ticket_with_id(ticket_service):
    ticket = ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    assert ticket.id == "CHEAP-0001"


def test_ticket_ids_increment(ticket_service):
    first = ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    second = ticket_service.submit_complaint("Beto", "beto@example.com", VALID_MESSAGE)
    assert first.id == "CHEAP-0001"
    assert second.id == "CHEAP-0002"


def test_empty_name_raises_value_error(ticket_service):
    with pytest.raises(ValueError):
        ticket_service.submit_complaint("   ", "ana@example.com", VALID_MESSAGE)


def test_invalid_email_raises_value_error(ticket_service):
    with pytest.raises(ValueError):
        ticket_service.submit_complaint("Ana", "ana-sin-arroba.com", VALID_MESSAGE)


def test_short_message_raises_value_error(ticket_service):
    with pytest.raises(ValueError):
        ticket_service.submit_complaint("Ana", "ana@example.com", "corto")


def test_premium_gets_high_priority(ticket_service):
    ticket = ticket_service.submit_complaint(
        "Ana", "ana@example.com", VALID_MESSAGE, is_premium=True
    )
    assert ticket.priority == "alta"


def test_urgent_message_gets_high_priority(ticket_service):
    ticket = ticket_service.submit_complaint(
        "Ana", "ana@example.com", "Esto es URGENTE, necesito ayuda ya."
    )
    assert ticket.priority == "alta"


def test_frequent_complainer_gets_medium_priority(ticket_service):
    for _ in range(4):
        ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    fifth = ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    assert fifth.previous_tickets == 4
    assert fifth.priority == "media"


def test_exactly_three_previous_tickets_stays_low_priority(ticket_service):
    for _ in range(3):
        ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    fourth = ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    assert fourth.previous_tickets == 3
    assert fourth.priority == "baja"


def test_default_priority_is_low(ticket_service):
    ticket = ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    assert ticket.priority == "baja"


def test_spanish_auto_reply_by_default(ticket_service):
    ticket = ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    assert ticket.auto_reply == "Recibimos tu reclamo. Hara fila con los demas problemas baratos."


def test_english_auto_reply(ticket_service):
    ticket = ticket_service.submit_complaint(
        "Ana", "ana@example.com", VALID_MESSAGE, language="en"
    )
    assert "queue" in ticket.auto_reply


def test_english_auto_reply_high_priority(ticket_service):
    ticket = ticket_service.submit_complaint(
        "Ana", "ana@example.com", VALID_MESSAGE, is_premium=True, language="en"
    )
    assert "fire" in ticket.auto_reply


def test_english_auto_reply_medium_priority(ticket_service):
    for _ in range(4):
        ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    ticket = ticket_service.submit_complaint(
        "Ana", "ana@example.com", VALID_MESSAGE, language="en"
    )
    assert "frequent flyer" in ticket.auto_reply


def test_tickets_for_filters_by_email(ticket_service):
    ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)
    ticket_service.submit_complaint("Beto", "beto@example.com", VALID_MESSAGE)
    ticket_service.submit_complaint("Ana", "ana@example.com", VALID_MESSAGE)

    ana_tickets = ticket_service.tickets_for("ana@example.com")
    assert len(ana_tickets) == 2
    assert all(t.email == "ana@example.com" for t in ana_tickets)


def test_tickets_for_unknown_email_is_empty(ticket_service):
    assert ticket_service.tickets_for("nadie@example.com") == []
