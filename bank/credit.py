"""Модуль с классом Кредит."""
from bank.base import BankProduct


class Credit(BankProduct):
    """Банковский кредит с аннуитетными платежами."""

    PRODUCT_NAME = "Кредит"

    def __init__(self, amount: float, annual_rate: float, months: int):
        super().__init__(amount, months)
        if annual_rate < 0:
            raise ValueError("Ставка не может быть отрицательной")
        self._annual_rate = float(annual_rate)

    # ================== managed-атрибуты ==================
    @property
    def annual_rate(self) -> float:
        return self._annual_rate

    @annual_rate.setter
    def annual_rate(self, value: float):
        if value < 0:
            raise ValueError("Ставка не может быть отрицательной")
        self._annual_rate = float(value)

    @property
    def monthly_rate(self) -> float:
        """Месячная ставка (доля, не проценты)."""
        return self._annual_rate / 12 / 100

    # ================== реализация абстрактных методов ==================
    def monthly_payment(self) -> float:
        """Аннуитетный платёж."""
        r = self.monthly_rate
        n = self._months
        if r == 0:
            return round(self._amount / n, 2)
        coeff = (r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return round(self._amount * coeff, 2)

    def total_amount(self) -> float:
        return round(self.monthly_payment() * self._months, 2)

    def payment_schedule(self) -> list[dict]:
        r = self.monthly_rate
        balance = self._amount
        payment = self.monthly_payment()
        schedule = []
        for month in range(1, self._months + 1):
            interest = round(balance * r, 2)
            principal = round(payment - interest, 2)
            balance = round(balance - principal, 2)
            if month == self._months:
                balance = 0.0
            schedule.append({
                "month": month,
                "payment": payment,
                "interest": interest,
                "principal": principal,
                "balance": max(balance, 0.0),
            })
        return schedule

    # ================== дополнительные свойства ==================
    @property
    def overpayment(self) -> float:
        """Переплата по кредиту."""
        return round(self.total_amount() - self._amount, 2)

    # ================== dunder-методы ==================
    def __str__(self) -> str:
        return (f"Кредит: {self._amount:,.2f} ₽ на {self._months} мес. "
                f"под {self._annual_rate}% → платёж {self.monthly_payment():,.2f} ₽")

    def __repr__(self) -> str:
        return (f"Credit(amount={self._amount}, "
                f"annual_rate={self._annual_rate}, months={self._months})")