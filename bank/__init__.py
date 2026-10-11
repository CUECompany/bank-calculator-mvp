"""Пакет банковских продуктов."""
from bank.base import BankProduct
from bank.credit import Credit
from bank.installment import Installment
from bank.deposit import Deposit

__all__ = ["BankProduct", "Credit", "Installment", "Deposit"]