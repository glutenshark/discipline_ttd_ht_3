import pytest
from hypothesis import given, strategies as st
from math import isclose

import task_manager


def test_calculate_invoice_success():
    """
    Проверяет корректность расчёта при валидных данных.

    Проверяются базовые случаи:
    - 10 часов × 20 = 200
    - 2.5 часа × 100 = 250
    """
    assert task_manager.calculate_invoice(10, 20, "USD") == 200
    assert task_manager.calculate_invoice(2.5, 100, "EUR") == 250


def test_calculate_invoice_zero():
    """
    Проверяет расчёт при нуле в часах или ставке.

    Ожидается результат 0.
    """
    assert task_manager.calculate_invoice(0, 50, "GBP") == 0
    assert task_manager.calculate_invoice(3, 0, "RUB") == 0


def test_calculate_invoice_negative():
    """
    Проверяет, что при отрицательных входных значениях
    вызывается ValueError.
    """
    with pytest.raises(ValueError):
        task_manager.calculate_invoice(-1, 10, "USD")
    with pytest.raises(ValueError):
        task_manager.calculate_invoice(5, -10, "USD")


def test_calculate_invoice_unsupported():
    """
    Проверяет реакцию на неподдерживаемую валюту.

    Ожидается ValueError.
    """
    with pytest.raises(ValueError):
        task_manager.calculate_invoice(1, 1, "XXX")


@given(
    hours=st.floats(min_value=0, max_value=1000),
    rate=st.floats(min_value=0, max_value=1000),
    currency=st.sampled_from(["USD", "EUR", "GBP", "RUB"])
)
def test_calculate_invoice_property(hours, rate, currency):
    """
    Генеративный тест: invoice = hours * rate
    при валидных входных значениях.

    Проверяется близость результатов с помощью isclose().
    """
    result = task_manager.calculate_invoice(hours, rate, currency)
    expected = hours * rate
    assert isclose(result, expected, rel_tol=1e-7)
