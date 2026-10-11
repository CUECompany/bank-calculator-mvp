"""Тесты для класса Deposit."""
import pytest
from bank.deposit import Deposit


class TestDepositInit:
    def test_valid_init(self):
        d = Deposit(100_000, 8, 12)
        assert d.amount == 100_000
        assert d.annual_rate == 8
        assert d.months == 12

    def test_negative_amount(self):
        with pytest.raises(ValueError):
            Deposit(-100, 8, 12)

    def test_negative_rate(self):
        with pytest.raises(ValueError):
            Deposit(100_000, -1, 12)


class TestDepositCalculations:
    def test_zero_rate(self):
        d = Deposit(100_000, 0, 12)
        assert d.total_amount() == 100_000.0
        assert d.income == 0.0

    def test_growth(self):
        d = Deposit(100_000, 12, 12)
        assert d.total_amount() > 100_000
        assert d.income > 0

    def test_capitalization(self):
        """С капитализацией итог больше простого процента."""
        d = Deposit(100_000, 12, 12)
        # простой процент: 100000 * (1 + 0.12) = 112000
        assert d.total_amount() > 112_000

    def test_schedule_length(self):
        d = Deposit(100_000, 8, 12)
        assert len(d.payment_schedule()) == 12

    def test_schedule_growing(self):
        d = Deposit(100_000, 8, 12)
        balances = [row["balance"] for row in d.payment_schedule()]
        assert balances == sorted(balances)  # неубывающая


class TestDepositDunder:
    def test_str(self):
        d = Deposit(100_000, 8, 12)
        assert "Вклад" in str(d)

    def test_repr(self):
        d = Deposit(100_000, 8, 12)
        assert "Deposit" in repr(d)

    def test_eq(self):
        d1 = Deposit(100_000, 8, 12)
        d2 = Deposit(100_000, 8, 12)
        assert d1 == d2

    def test_len(self):
        d = Deposit(100_000, 8, 12)
        assert len(d) == 12


class TestDepositVsCredit:
    def test_different_types_not_equal(self):
        from bank.credit import Credit
        d = Deposit(100_000, 8, 12)
        c = Credit(100_000, 8, 12)
        assert d != c