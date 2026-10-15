import pytest

from cheapgpt.support.excuses import Customer, ExcuseService


def _customer(plan="gratis", months_as_customer=0):
    return Customer(name="Ana", plan=plan, months_as_customer=months_as_customer)


def test_full_excuse_text():
    excuse = ExcuseService().generate(_customer(), "chat", "grave", 3)
    assert excuse.text == (
        "Estimado/a Ana: el chat esta caido hace 3 dia(s) porque el practicante hizo "
        "push directo a main. Por ser plan gratis, lo arreglaremos en 44 dias habiles. "
        "Compensacion: un sticker de cheapGPT."
    )


def test_excuse_numbers_increment():
    service = ExcuseService()
    first = service.generate(_customer(), "chat", "leve", 0)
    second = service.generate(_customer(), "chat", "leve", 0)
    assert (first.number, second.number) == (1, 2)


def test_minor_outage_on_plans_page():
    excuse = ExcuseService().generate(_customer("barato", 5), "planes", "leve", 0)
    assert excuse.reason == "el servidor se quedo dormido"
    assert excuse.repair_days == 4
    assert excuse.compensation == "un sticker de cheapGPT"


def test_minor_chat_outage_has_no_extra_day():
    excuse = ExcuseService().generate(_customer("premium_economico", 3), "chat", "leve", 1)
    assert excuse.reason == "el wifi de la oficina esta en modo ahorro de energia"
    assert excuse.repair_days == 3
    assert excuse.compensation == "una disculpa escrita a mano"


def test_serious_outage_outside_chat_has_no_extra_day():
    excuse = ExcuseService().generate(_customer("barato", 24), "planes", "grave", 0)
    assert excuse.reason == "el hamster que mueve el servidor pidio vacaciones"
    assert excuse.repair_days == 14
    assert excuse.compensation == "un sticker de cheapGPT autografiado"


def test_apocalyptic_outage_adds_alert_prefix():
    excuse = ExcuseService().generate(_customer("premium_economico", 12), "reclamos", "apocaliptica", 2)
    assert excuse.reason == "la IA tomo conciencia y renuncio"
    assert excuse.repair_days == 32
    assert excuse.compensation == "un mes gratis (de un plan que ya es casi gratis)"
    assert excuse.text.startswith("ALERTA MAXIMA: Estimado/a Ana: el sistema de reclamos esta caido")


def test_new_customers_wait_longer():
    new = ExcuseService().generate(_customer("barato", 0), "planes", "leve", 0)
    old = ExcuseService().generate(_customer("barato", 1), "planes", "leve", 0)
    assert (new.repair_days, old.repair_days) == (6, 4)


def test_premium_with_eleven_months_gets_only_an_apology():
    excuse = ExcuseService().generate(_customer("premium_economico", 11), "chat", "leve", 0)
    assert excuse.compensation == "una disculpa escrita a mano"


def test_twenty_three_months_gets_a_regular_sticker():
    excuse = ExcuseService().generate(_customer("gratis", 23), "chat", "leve", 0)
    assert excuse.compensation == "un sticker de cheapGPT"


def test_most_affected_service():
    service = ExcuseService()
    assert service.most_affected_service() is None
    service.generate(_customer(), "planes", "leve", 0)
    service.generate(_customer(), "chat", "leve", 0)
    service.generate(_customer(), "planes", "grave", 1)
    assert service.most_affected_service() == "planes"


@pytest.mark.parametrize(
    "customer, service, severity, days_down",
    [
        (Customer("Ana", "gratis", 0), "correo", "leve", 0),
        (Customer("Ana", "gratis", 0), "chat", "catastrofica", 0),
        (Customer("Ana", "gratis", 0), "chat", "leve", -1),
        (Customer("Ana", "platino", 0), "chat", "leve", 0),
    ],
)
def test_invalid_input_raises_value_error(customer, service, severity, days_down):
    with pytest.raises(ValueError):
        ExcuseService().generate(customer, service, severity, days_down)


def test_invalid_excuse_is_not_counted():
    service = ExcuseService()
    with pytest.raises(ValueError):
        service.generate(_customer(), "chat", "catastrofica", 0)
    assert service.most_affected_service() is None
    assert service.generate(_customer(), "chat", "leve", 0).number == 1
