"""Тесты для класса Credit."""
import pytest
from bank.credit import Credit


class TestCreditInit:
    def test_valid_init(self):
        c = Credit(100_000, 15, 12)
        assert c.amount == 100_000
        assert c.annual_rate == 15
        assert c.months == 12

    def test_negative_amount(self):
        with pytest.raises(ValueError):
            Credit(-100, 15, 12)

    def test_negative_rate(self):
        with pytest.raises(ValueError):
            Credit(100_000, -5, 12)

    def test_zero_months(self):
        with pytest.raises(ValueError):
            Credit(100_000, 15, 0)


class TestCreditCalculations:
    def test_zero_rate(self):
        """Без процентов платёж = сумма / срок."""
        c = Credit(120_000, 0, 12)
        assert c.monthly_payment() == 10_000.0
        assert c.overpayment == 0.0

    def test_monthly_payment_positive(self):
        c = Credit(100_000, 15, 12)
        assert c.monthly_payment() > 0

    def test_overpayment_positive(self):
        c = Credit(100_000, 15, 12)
        assert c.overpayment > 0

    def test_total_equals_payments_sum(self):
        c = Credit(100_000, 15, 12)
        assert c.total_amount() == pytest.approx(c.monthly_payment() * 12, abs=0.1)

    def test_schedule_length(self):
        c = Credit(100_000, 15, 12)
        assert len(c.payment_schedule()) == 12

    def test_schedule_last_balance_zero(self):
        c = Credit(100_000, 15, 12)
        schedule = c.payment_schedule()
        assert schedule[-1]["balance"] == 0.0

    def test_schedule_first_has_interest(self):
        c = Credit(100_000, 15, 12)
        first = c.payment_schedule()[0]
        assert first["interest"] > 0
        assert first["principal"] > 0


class TestCreditProperties:
    def test_rate_setter(self):
        c = Credit(100_000, 15, 12)
        c.annual_rate = 20
        assert c.annual_rate == 20

    def test_rate_setter_negative(self):
        c = Credit(100_000, 15, 12)
        with pytest.raises(ValueError):
            c.annual_rate = -5

    def test_amount_setter(self):
        c = Credit(100_000, 15, 12)
        c.amount = 200_000
        assert c.amount == 200_000


class TestCreditDunder:
    def test_str(self):
        c = Credit(100_000, 15, 12)
        assert "Кредит" in str(c)
        assert "100,000" in str(c)

    def test_repr(self):
        c = Credit(100_000, 15, 12)
        assert "Credit" in repr(c)

    def test_eq(self):
        c1 = Credit(100_000, 15, 12)
        c2 = Credit(100_000, 15, 12)
        assert c1 == c2

    def test_not_eq_different_class(self):
        from bank.deposit import Deposit
        c = Credit(100_000, 15, 12)
        d = Deposit(100_000, 15, 12)
        assert c != d

    def test_len(self):
        c = Credit(100_000, 15, 12)
        assert len(c) == 12