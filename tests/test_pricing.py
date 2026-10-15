import pytest

from cheapgpt.billing.pricing import calculate_plan_price


def test_gratis_plan_is_always_zero():
    assert calculate_plan_price("gratis", 1) == 0
    assert calculate_plan_price("gratis", 12) == 0


def test_barato_one_month_no_discount():
    assert calculate_plan_price("barato", 1) == 5938


def test_barato_five_months_no_discount():
    assert calculate_plan_price("barato", 5) == 29690


def test_barato_six_months_gets_discount():
    assert calculate_plan_price("barato", 6) == 33847


def test_barato_eleven_months_keeps_six_month_discount():
    assert calculate_plan_price("barato", 11) == 62053


def test_barato_twelve_months_gets_max_discount():
    assert calculate_plan_price("barato", 12) == 60569


def test_premium_economico_one_month():
    assert calculate_plan_price("premium_economico", 1) == 11888


def test_premium_economico_six_months():
    assert calculate_plan_price("premium_economico", 6) == 67762


def test_premium_economico_twelve_months():
    assert calculate_plan_price("premium_economico", 12) == 121259


def test_invalid_plan_raises_value_error():
    with pytest.raises(ValueError):
        calculate_plan_price("inexistente", 1)


def test_zero_months_raises_value_error():
    with pytest.raises(ValueError):
        calculate_plan_price("barato", 0)


def test_negative_months_raises_value_error():
    with pytest.raises(ValueError):
        calculate_plan_price("barato", -3)
