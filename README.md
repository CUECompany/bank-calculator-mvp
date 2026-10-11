Лабораторная работа №2. Модули и пакеты Python. ООП.
Вариант 14. Банковские услуги: кредит, рассрочка, вклад.

Описание

Bank Calculator MVP — банковский калькулятор с графическим интерфейсом на PySide6. Проект демонстрирует принципы объектно-ориентированного программирования на Python: абстрактные базовые классы, наследование, managed-атрибуты через property, dunder-методы.

Функциональность

Кредит — расчёт аннуитетного платежа, переплаты и графика платежей по месяцам.
Рассрочка — расчёт ежемесячного платежа с учётом комиссии.
Вклад — расчёт дохода с ежемесячной капитализацией процентов.
Экспорт отчётов в форматы docx и xlsx.
Покрытие тестами через pytest.
Тёмная тема интерфейса.

Архитектура

Абстрактный базовый класс BankProduct с методами monthly_payment, total_amount, payment_schedule. От него наследуются три класса: Credit, Installment, Deposit.

Структура проекта

bank_mvp/
bank/
init.py
base.py
credit.py
installment.py
deposit.py
tests/
init.py
test_base.py
test_credit.py
test_installment.py
test_deposit.py
styles.py
main.py
report_generator.py
pytest.ini
requirements.txt
README.md

Запуск

Клонировать репозиторий:
git clone https://github.com/CUECompany/bank-calculator-mvp.git
cd bank-calculator-mvp

Создать виртуальное окружение (Windows):
python -m venv .venv
.venv\Scripts\activate

Установить зависимости:
pip install -r requirements.txt

Запустить приложение:
python main.py
