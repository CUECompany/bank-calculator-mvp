"""Модуль с классом Вклад."""
from bank.base import BankProduct


class Deposit(BankProduct):
    """Вклад со сложным процентом (капитализация ежемесячно)."""

    PRODUCT_NAME = "Вклад"

    def __init__(self, amount: float, annual_rate: float, months: int):
        super().__init__(amount, months)
        if annual_rate < 0:
            raise ValueError("Ставка не может быть отрицательной")
        self._annual_rate = float(annual_rate)

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
        return self._annual_rate / 12 / 100

    # ================== реализация абстрактных методов ==================
    def monthly_payment(self) -> float:
        """Для вклада — доход за месяц (усреднённый)."""
        return round(self.income / self._months, 2)

    def total_amount(self) -> float:
        """Итоговая сумма вклада с капитализацией."""
        return round(self._amount * (1 + self.monthly_rate) ** self._months, 2)

    def payment_schedule(self) -> list[dict]:
        """Рост вклада по месяцам."""
        schedule = []
        balance = self._amount
        for month in range(1, self._months + 1):
            balance = round(balance * (1 + self.monthly_rate), 2)
            schedule.append({"month": month, "balance": balance})
        return schedule

    @property
    def income(self) -> float:
        """Доход по вкладу."""
        return round(self.total_amount() - self._amount, 2)

    # ================== dunder-методы ==================
    def __str__(self) -> str:
        return (f"Вклад: {self._amount:,.2f} ₽ на {self._months} мес. "
                f"под {self._annual_rate}% → доход {self.income:,.2f} ₽")

    def __repr__(self) -> str:
        return (f"Deposit(amount={self._amount}, "
                f"annual_rate={self._annual_rate}, months={self._months})")