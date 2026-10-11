"""Тесты для абстрактного базового класса BankProduct."""
import pytest
from bank.base import BankProduct


def test_cannot_instantiate_abstract():
    """Нельзя создать экземпляр абстрактного класса."""
    with pytest.raises(TypeError):
        BankProduct(1000, 12)


def test_concrete_subclass_must_implement_methods():
    """Подкласс без реализации абстрактных методов не создаётся."""

    class Incomplete(BankProduct):
        PRODUCT_NAME = "Неполный"

    with pytest.raises(TypeError):
        Incomplete(1000, 12)