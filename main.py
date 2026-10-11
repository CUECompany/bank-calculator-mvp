"""GUI на PySide6 для банковского калькулятора."""
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTextEdit,
    QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem,
    QFrame, QSizePolicy, QHeaderView
)

from bank import Credit, Installment, Deposit
from report_generator import save_to_docx, save_to_xlsx
from styles import STYLESHEET, COLORS


class Card(QFrame):
    """Карточка с заголовком и содержимым."""
    def __init__(self, title: str):
        super().__init__()
        self.setObjectName("Card")
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(16, 14, 16, 16)
        self._layout.setSpacing(10)

        title_lbl = QLabel(title)
        title_lbl.setObjectName("CardTitle")
        self._layout.addWidget(title_lbl)

    def add_widget(self, w):
        self._layout.addWidget(w)

    def add_layout(self, l):
        self._layout.addLayout(l)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bank Calculator — Вариант 14")
        self.resize(1080, 780)
        self.current_data = None

        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ===== Шапка =====
        header = QFrame()
        header.setObjectName("HeaderFrame")
        hlay = QHBoxLayout(header)
        hlay.setContentsMargins(24, 16, 24, 16)

        left = QVBoxLayout()
        left.setSpacing(2)
        title = QLabel("Bank Calculator")
        title.setObjectName("AppTitle")
        subtitle = QLabel("Кредит · Рассрочка · Вклад — расчёт платежей и доходности")
        subtitle.setObjectName("AppSubtitle")
        left.addWidget(title)
        left.addWidget(subtitle)

        hlay.addLayout(left)
        hlay.addStretch()  

        root.addWidget(header)

        # ===== Основной контент =====
        content = QWidget()
        cl = QHBoxLayout(content)
        cl.setContentsMargins(20, 18, 20, 20)
        cl.setSpacing(16)

        # --- Левая колонка: параметры ---
        left_col = QVBoxLayout()
        left_col.setSpacing(14)

        params_card = Card("⚙  Параметры расчёта")
        # Тип продукта
        type_row = QHBoxLayout()
        type_row.addWidget(QLabel("Тип продукта:"))
        self.product_type = QComboBox()
        self.product_type.addItems(["Кредит", "Рассрочка", "Вклад"])
        self.product_type.currentIndexChanged.connect(self.on_type_changed)
        type_row.addWidget(self.product_type, 1)
        params_card.add_layout(type_row)

        # Поля ввода
        self.inputs_container = QVBoxLayout()
        self.inputs_container.setSpacing(8)
        params_card.add_layout(self.inputs_container)

        self.inputs = {}
        self._build_inputs()

        # Кнопки
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        self.btn_calc = QPushButton("  Рассчитать")
        self.btn_calc.setMinimumHeight(38)
        self.btn_calc.clicked.connect(self.calculate)

        self.btn_docx = QPushButton("  Сохранить .docx")
        self.btn_docx.setObjectName("Secondary")
        self.btn_docx.setMinimumHeight(38)
        self.btn_docx.clicked.connect(lambda: self.save("docx"))

        self.btn_xlsx = QPushButton("  Сохранить .xlsx")
        self.btn_xlsx.setObjectName("Secondary")
        self.btn_xlsx.setMinimumHeight(38)
        self.btn_xlsx.clicked.connect(lambda: self.save("xlsx"))

        btn_row.addWidget(self.btn_calc, 2)
        btn_row.addWidget(self.btn_docx, 1)
        btn_row.addWidget(self.btn_xlsx, 1)
        params_card.add_layout(btn_row)

        left_col.addWidget(params_card)
        left_col.addStretch()

        # --- Правая колонка: результаты + график ---
        right_col = QVBoxLayout()
        right_col.setSpacing(14)

        result_card = Card("Результаты")
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(180)
        result_card.add_widget(self.result_text)
        right_col.addWidget(result_card)

        schedule_card = Card("График платежей")
        self.schedule_table = QTableWidget()
        self.schedule_table.setAlternatingRowColors(True)
        self.schedule_table.verticalHeader().setVisible(False)
        self.schedule_table.horizontalHeader().setStretchLastSection(True)
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.setMinimumHeight(280)
        schedule_card.add_widget(self.schedule_table)
        right_col.addWidget(schedule_card, 1)

        cl.addLayout(left_col, 4)
        cl.addLayout(right_col, 6)

        root.addWidget(content)

        # Применяем QSS
        self.setStyleSheet(STYLESHEET)

    # ================= Поля ввода =================
    def _build_inputs(self):
        while self.inputs_container.count():
            item = self.inputs_container.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self.inputs.clear()

        product = self.product_type.currentText()

        def add_field(label_text, key, default):
            row = QHBoxLayout()
            lbl = QLabel(label_text)
            lbl.setMinimumWidth(140)
            le = QLineEdit(str(default))
            le.setPlaceholderText("Введите значение…")
            self.inputs[key] = le
            row.addWidget(lbl)
            row.addWidget(le, 1)
            container = QWidget()
            container.setLayout(row)
            self.inputs_container.addWidget(container)

        add_field("Сумма (₽):", "amount", "100000")
        add_field("Срок (месяцев):", "months", "12")

        if product == "Кредит":
            add_field("Годовая ставка (%):", "rate", "15")
        elif product == "Рассрочка":
            add_field("Комиссия (%):", "commission", "5")
        elif product == "Вклад":
            add_field("Годовая ставка (%):", "rate", "8")

    def on_type_changed(self):
        self._build_inputs()
        self.result_text.clear()
        self.schedule_table.clear()
        self.schedule_table.setRowCount(0)
        self.schedule_table.setColumnCount(0)

    # ================= Утилиты ввода =================
    def _get_float(self, key):
        try:
            return float(self.inputs[key].text().replace(",", "."))
        except ValueError:
            raise ValueError(f"Некорректное значение в поле '{key}'")

    def _get_int(self, key):
        try:
            return int(self.inputs[key].text())
        except ValueError:
            raise ValueError(f"Некорректное значение в поле '{key}'")

    # ================= Расчёт =================
    def calculate(self):
        try:
            product = self.product_type.currentText()
            amount = self._get_float("amount")
            months = self._get_int("months")

            if product == "Кредит":
                rate = self._get_float("rate")
                obj = Credit(amount, rate, months)
                text = self._format_result(
                    title="КРЕДИТ",
                    rows=[
                        ("Сумма", f"{amount:,.2f} ₽"),
                        ("Срок", f"{months} мес."),
                        ("Ставка", f"{rate}% годовых"),
                        ("───", ""),
                        ("Месячный платёж", f"{obj.monthly_payment():,.2f} ₽"),
                        ("Общая выплата", f"{obj.total_amount():,.2f} ₽"),
                    ],
                    accent=("Переплата", f"{obj.overpayment:,.2f} ₽", COLORS['danger']),
                )
                params = {"Сумма": amount, "Срок (мес.)": months, "Ставка (%)": rate}
                results = {
                    "Месячный платёж": obj.monthly_payment(),
                    "Общая выплата": obj.total_amount(),
                    "Переплата": obj.overpayment,
                }
                schedule = obj.payment_schedule()

            elif product == "Рассрочка":
                commission = self._get_float("commission")
                obj = Installment(amount, months, commission)
                text = self._format_result(
                    title="РАССРОЧКА",
                    rows=[
                        ("Сумма", f"{amount:,.2f} ₽"),
                        ("Срок", f"{months} мес."),
                        ("Комиссия", f"{commission}%  ({obj.commission_amount:,.2f} ₽)"),
                        ("───", ""),
                        ("Месячный платёж", f"{obj.monthly_payment():,.2f} ₽"),
                    ],
                    accent=("Итого к оплате", f"{obj.total_amount():,.2f} ₽", COLORS['warning']),
                )
                params = {"Сумма": amount, "Срок (мес.)": months, "Комиссия (%)": commission}
                results = {
                    "Комиссия (₽)": obj.commission_amount,
                    "Месячный платёж": obj.monthly_payment(),
                    "Итого": obj.total_amount(),
                }
                schedule = obj.payment_schedule()

            else:  # Вклад
                rate = self._get_float("rate")
                obj = Deposit(amount, rate, months)
                text = self._format_result(
                    title="ВКЛАД",
                    rows=[
                        ("Сумма", f"{amount:,.2f} ₽"),
                        ("Срок", f"{months} мес."),
                        ("Ставка", f"{rate}% годовых (капитализация)"),
                        ("───", ""),
                        ("Итоговая сумма", f"{obj.total_amount():,.2f} ₽"),
                    ],
                    accent=("Доход", f"+{obj.income:,.2f} ₽", COLORS['success']),
                )
                params = {"Сумма": amount, "Срок (мес.)": months, "Ставка (%)": rate}
                results = {
                    "Итоговая сумма": obj.total_amount(),
                    "Доход": obj.income,
                }
                schedule = obj.payment_schedule()

            self.result_text.setHtml(text)
            self.current_data = {"params": params, "results": results, "schedule": schedule}
            self._fill_table(schedule)

        except ValueError as e:
            QMessageBox.warning(self, "Ошибка ввода", str(e))

    def _format_result(self, title, rows, accent):
        """Красивый HTML-вывод результата."""
        html = f"<div style='font-size:12pt; font-weight:700; color:{COLORS['primary']};'>"
        html += f"{title}</div><br>"
        for k, v in rows:
            if k == "───":
                html += f"<div style='color:{COLORS['border']};'>───────────────</div>"
            else:
                html += (f"<div style='color:{COLORS['text_muted']};'>{k}: "
                         f"<span style='color:{COLORS['text']}; font-weight:600;'>{v}</span></div>")
        html += "<br>"
        label, value, color = accent
        html += (f"<div style='font-size:12pt; font-weight:700; color:{color};'>"
                 f"{label}: {value}</div>")
        return html

    # ================= Таблица =================
    def _fill_table(self, schedule):
        if not schedule:
            self.schedule_table.clear()
            self.schedule_table.setRowCount(0)
            self.schedule_table.setColumnCount(0)
            return
        headers = list(schedule[0].keys())
        self.schedule_table.setColumnCount(len(headers))
        self.schedule_table.setHorizontalHeaderLabels([h.capitalize() for h in headers])
        self.schedule_table.setRowCount(len(schedule))
        for r, row in enumerate(schedule):
            for c, value in enumerate(row.values()):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.schedule_table.setItem(r, c, item)

    # ================= Сохранение =================
    def save(self, fmt):
        if not self.current_data:
            QMessageBox.warning(self, "Нет данных", "Сначала выполните расчёт.")
            return
        if fmt == "docx":
            path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить .docx", "report.docx", "*.docx")
            if path:
                save_to_docx(self.current_data, path)
                QMessageBox.information(self, "Готово", f"Сохранено:\n{path}")
        else:
            path, _ = QFileDialog.getSaveFileName(
                self, "Сохранить .xlsx", "report.xlsx", "*.xlsx")
            if path:
                save_to_xlsx(self.current_data, path)
                QMessageBox.information(self, "Готово", f"Сохранено:\n{path}")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()