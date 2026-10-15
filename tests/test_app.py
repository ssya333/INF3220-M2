def test_get_chat_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_post_chat_shows_fake_reply(client):
    response = client.post("/", data={"mood": "chistoso", "message": "hola"})
    assert response.status_code == 200
    assert "Tu asistente de confianza" in response.get_data(as_text=True)


def test_get_plans_page(client):
    response = client.get("/planes")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert "Gratis" in body
    assert "Barato" in body


def test_get_complaint_page(client):
    response = client.get("/reclamo")
    assert response.status_code == 200


def test_post_complaint_shows_ticket_id(client):
    response = client.post(
        "/reclamo",
        data={
            "name": "Ana",
            "email": "ana@example.com",
            "message": "Tengo un problema con el servicio, ayuda por favor.",
        },
    )
    assert response.status_code == 200
    assert "CHEAP-" in response.get_data(as_text=True)


def test_post_complaint_with_invalid_data_shows_error(client):
    response = client.post(
        "/reclamo",
        data={"name": "", "email": "ana@example.com", "message": "algo"},
    )
    assert response.status_code == 200
    assert "Error" in response.get_data(as_text=True)


def _app_on(day):
    from datetime import datetime

    from cheapgpt.app import create_app
    from cheapgpt.llm.client import FakeLLMClient

    app = create_app(llm=FakeLLMClient(), clock=lambda: datetime(2030, 1, day, 12, 0, 0))
    app.testing = True
    return app.test_client()


def test_post_chat_shows_remaining_messages():
    client = _app_on(1)
    response = client.post("/", data={"mood": "chistoso", "plan": "gratis", "message": "hola"})
    assert "Te quedan 3 mensaje(s) hoy" in response.get_data(as_text=True)


def test_post_chat_after_four_free_messages_shows_quota_error():
    client = _app_on(2)
    for _ in range(4):
        client.post("/", data={"mood": "chistoso", "plan": "gratis", "message": "hola"})
    response = client.post("/", data={"mood": "chistoso", "plan": "gratis", "message": "otro"})
    body = response.get_data(as_text=True)
    assert "Se acabaron tus mensajes de hoy" in body
    assert "otro" not in body


def test_post_chat_with_invalid_plan_shows_error():
    client = _app_on(3)
    response = client.post("/", data={"mood": "chistoso", "plan": "platino", "message": "hola"})
    assert "Plan invalido" in response.get_data(as_text=True)


def test_get_excuses_page(client):
    response = client.get("/excusas")
    assert response.status_code == 200
    assert "Girar la ruleta" in response.get_data(as_text=True)


def test_post_excuses_shows_excuse(client):
    response = client.post(
        "/excusas",
        data={
            "name": "Ana",
            "plan": "gratis",
            "months_as_customer": "0",
            "service": "chat",
            "severity": "grave",
            "days_down": "3",
        },
    )
    body = response.get_data(as_text=True)
    assert response.status_code == 200
    assert "Excusa oficial N° 001" in body
    assert "44 dias habiles" in body
    assert "Servicio mas caido hoy: el chat" in body


def test_post_excuses_with_invalid_data_shows_error(client):
    response = client.post(
        "/excusas",
        data={
            "name": "Ana",
            "plan": "gratis",
            "months_as_customer": "0",
            "service": "chat",
            "severity": "grave",
            "days_down": "-1",
        },
    )
    assert "Error" in response.get_data(as_text=True)
