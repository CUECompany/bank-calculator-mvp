"""Тесты для класса Installment."""
import pytest
from bank.installment import Installment


class TestInstallmentInit:
    def test_valid_init(self):
        i = Installment(50_000, 6, 5)
        assert i.amount == 50_000
        assert i.months == 6
        assert i.commission_percent == 5

    def test_zero_commission_default(self):
        i = Installment(50_000, 6)
        assert i.commission_percent == 0.0

    def test_negative_amount(self):
        with pytest.raises(ValueError):
            Installment(-100, 6, 5)

    def test_negative_commission(self):
        with pytest.raises(ValueError):
            Installment(50_000, 6, -1)


class TestInstallmentCalculations:
    def test_zero_commission(self):
        i = Installment(60_000, 6, 0)
        assert i.commission_amount == 0
        assert i.total_amount() == 60_000
        assert i.monthly_payment() == 10_000.0

    def test_with_commission(self):
        i = Installment(100_000, 10, 10)
        assert i.commission_amount == 10_000
        assert i.total_amount() == 110_000
        assert i.monthly_payment() == 11_000.0

    def test_schedule_length(self):
        i = Installment(50_000, 6, 5)
        assert len(i.payment_schedule()) == 6


class TestInstallmentDunder:
    def test_str(self):
        i = Installment(50_000, 6, 5)
        assert "Рассрочка" in str(i)

    def test_repr(self):
        i = Installment(50_000, 6, 5)
        assert "Installment" in repr(i)

    def test_eq(self):
        i1 = Installment(50_000, 6, 5)
        i2 = Installment(50_000, 6, 5)
        assert i1 == i2

    def test_len(self):
        i = Installment(50_000, 6, 5)
        assert len(i) == 6