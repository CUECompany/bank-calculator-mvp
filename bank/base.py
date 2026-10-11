"""Абстрактный базовый класс банковского продукта."""
from abc import ABC, abstractmethod


class BankProduct(ABC):
    """Абстрактный банковский продукт.

    Все банковские продукты (кредит, рассрочка, вклад) наследуются от
    этого класса и обязаны реализовать методы:
        - monthly_payment  — размер регулярного платежа/выплаты
        - total_amount     — итоговая сумма по продукту
        - payment_schedule — график платежей
    """

    #: Человекочитаемое название продукта (переопределяется в наследниках)
    PRODUCT_NAME: str = "Продукт"

    def __init__(self, amount: float, months: int):
        if amount <= 0:
            raise ValueError("Сумма должна быть положительной")
        if months <= 0:
            raise ValueError("Срок должен быть положительным")

        # protected-атрибуты (managed через property)
        self._amount = float(amount)
        self._months = int(months)

    # ================== managed-атрибуты ==================
    @property
    def amount(self) -> float:
        """Сумма продукта."""
        return self._amount

    @amount.setter
    def amount(self, value: float):
        if value <= 0:
            raise ValueError("Сумма должна быть положительной")
        self._amount = float(value)

    @property
    def months(self) -> int:
        """Срок в месяцах."""
        return self._months

    @months.setter
    def months(self, value: int):
        if value <= 0:
            raise ValueError("Срок должен быть положительным")
        self._months = int(value)

    # ================== абстрактные методы ==================
    @abstractmethod
    def monthly_payment(self) -> float:
        """Размер регулярного платежа."""
        ...

    @abstractmethod
    def total_amount(self) -> float:
        """Итоговая сумма по продукту."""
        ...

    @abstractmethod
    def payment_schedule(self) -> list[dict]:
        """График платежей/начислений."""
        ...

    # ================== dunder-методы ==================
    def __str__(self) -> str:
        return (f"{self.PRODUCT_NAME}: {self._amount:,.2f} ₽ "
                f"на {self._months} мес.")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(amount={self._amount}, months={self._months})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, BankProduct):
            return NotImplemented
        return (self.__class__ is other.__class__
                and self._amount == other._amount
                and self._months == other._months)

    def __hash__(self) -> int:
        return hash((self.__class__.__name__, self._amount, self._months))

    def __len__(self) -> int:
        """Срок в месяцах — удобно для len()."""
        return self._months