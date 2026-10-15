from datetime import datetime

import pytest

from cheapgpt.chat.quota import MessageQuota, QuotaExceededError

# Cada test usa un user_id distinto para no depender del estado de otros tests.


def _quota_at(day):
    return MessageQuota(clock=lambda: datetime(2024, 1, day, 12, 0, 0))


def test_free_plan_returns_remaining_messages():
    quota = _quota_at(1)
    assert quota.register_message("gratis-restantes", "gratis") == 3
    assert quota.register_message("gratis-restantes", "gratis") == 2


def test_free_plan_allows_four_messages_per_day():
    quota = _quota_at(1)
    for _ in range(3):
        quota.register_message("gratis-limite", "gratis")
    assert quota.register_message("gratis-limite", "gratis") == 0
    with pytest.raises(QuotaExceededError):
        quota.register_message("gratis-limite", "gratis")


def test_student_on_free_plan_gets_ten_messages():
    quota = _quota_at(1)
    assert quota.register_message("estudiante", "gratis", is_student=True) == 9
    for _ in range(8):
        quota.register_message("estudiante", "gratis", is_student=True)
    assert quota.register_message("estudiante", "gratis", is_student=True) == 0
    with pytest.raises(QuotaExceededError):
        quota.register_message("estudiante", "gratis", is_student=True)


def test_cheap_plan_allows_fifty_messages_per_day():
    quota = _quota_at(1)
    assert quota.register_message("barato-limite", "barato") == 49
    for _ in range(48):
        quota.register_message("barato-limite", "barato")
    assert quota.register_message("barato-limite", "barato") == 0
    with pytest.raises(QuotaExceededError):
        quota.register_message("barato-limite", "barato")


def test_student_benefit_does_not_apply_to_cheap_plan():
    quota = _quota_at(1)
    assert quota.register_message("barato-estudiante", "barato", is_student=True) == 49


def test_premium_plan_has_no_limit():
    quota = _quota_at(1)
    for _ in range(100):
        assert quota.register_message("premium", "premium_economico") is None


def test_quota_resets_the_next_day():
    first_day = _quota_at(1)
    for _ in range(4):
        first_day.register_message("gratis-dia", "gratis")
    with pytest.raises(QuotaExceededError):
        first_day.register_message("gratis-dia", "gratis")

    next_day = _quota_at(2)
    assert next_day.register_message("gratis-dia", "gratis") == 3


def test_users_have_independent_quotas():
    quota = _quota_at(1)
    for _ in range(4):
        quota.register_message("usuario-a", "gratis")
    assert quota.register_message("usuario-b", "gratis") == 3


def test_invalid_plan_raises_value_error():
    quota = _quota_at(1)
    with pytest.raises(ValueError):
        quota.register_message("plan-invalido", "platino")
