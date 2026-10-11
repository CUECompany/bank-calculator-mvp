"""Модуль с классом Рассрочка."""
from bank.base import BankProduct


class Installment(BankProduct):
    """Рассрочка с фиксированной комиссией."""

    PRODUCT_NAME = "Рассрочка"

    def __init__(self, amount: float, months: int, commission_percent: float = 0.0):
        super().__init__(amount, months)
        if commission_percent < 0:
            raise ValueError("Комиссия не может быть отрицательной")
        self._commission_percent = float(commission_percent)

    @property
    def commission_percent(self) -> float:
        return self._commission_percent

    @commission_percent.setter
    def commission_percent(self, value: float):
        if value < 0:
            raise ValueError("Комиссия не может быть отрицательной")
        self._commission_percent = float(value)

    @property
    def commission_amount(self) -> float:
        return round(self._amount * self._commission_percent / 100, 2)

    # ================== реализация абстрактных методов ==================
    def monthly_payment(self) -> float:
        return round(self.total_amount() / self._months, 2)

    def total_amount(self) -> float:
        return round(self._amount + self.commission_amount, 2)

    def payment_schedule(self) -> list[dict]:
        schedule = []
        total = self.total_amount()
        payment = self.monthly_payment()
        for month in range(1, self._months + 1):
            schedule.append({
                "month": month,
                "payment": payment,
                "remaining": round(total - payment * month, 2),
            })
        return schedule

    # ================== dunder-методы ==================
    def __str__(self) -> str:
        return (f"Рассрочка: {self._amount:,.2f} ₽ на {self._months} мес. "
                f"(комиссия {self._commission_percent}%) → "
                f"платёж {self.monthly_payment():,.2f} ₽")

    def __repr__(self) -> str:
        return (f"Installment(amount={self._amount}, months={self._months}, "
                f"commission_percent={self._commission_percent})")