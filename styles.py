"""Стили и палитра приложения."""

# --- Палитра ---
COLORS = {
    "bg":            "#0F1729",   # глубокий тёмно-синий
    "bg_card":       "#1A2438",   # карточки
    "bg_input":      "#232F47",   # поля ввода
    "bg_hover":      "#2C3A56",
    "primary":       "#4F8CFF",   # акцент (синий)
    "primary_hover": "#6BA0FF",
    "primary_press": "#3A72DC",
    "success":       "#22C55E",   # зелёный
    "warning":       "#F59E0B",   # оранжевый
    "danger":        "#EF4444",   # красный
    "text":          "#E6EDF7",
    "text_muted":    "#8B9AB3",
    "border":        "#2A3650",
    "header_grad1":  "#1E2A47",
    "header_grad2":  "#141C2E",
}


STYLESHEET = f"""
/* ---------- Общий фон ---------- */
QMainWindow, QWidget {{
    background-color: {COLORS['bg']};
    color: {COLORS['text']};
    font-family: "Segoe UI", "Inter", "Arial";
    font-size: 10.5pt;
}}

/* ---------- Заголовок окна (шапка) ---------- */
#HeaderFrame {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {COLORS['header_grad1']},
                stop:1 {COLORS['header_grad2']});
    border-bottom: 1px solid {COLORS['border']};
    border-radius: 0px;
}}

#AppTitle {{
    font-size: 18pt;
    font-weight: 700;
    color: {COLORS['text']};
    padding: 4px 0;
}}

#AppSubtitle {{
    font-size: 9.5pt;
    color: {COLORS['text_muted']};
    padding-bottom: 4px;
}}

#Badge {{
    background-color: {COLORS['primary']};
    color: white;
    border-radius: 10px;
    padding: 3px 10px;
    font-size: 9pt;
    font-weight: 600;
}}

/* ---------- Карточки ---------- */
#Card {{
    background-color: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    padding: 14px;
}}

#CardTitle {{
    font-size: 11pt;
    font-weight: 700;
    color: {COLORS['text']};
    padding-bottom: 6px;
}}

/* ---------- Поля ввода ---------- */
QLabel {{
    color: {COLORS['text']};
    font-size: 10pt;
    background: transparent;
}}

QLineEdit, QComboBox {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 8px 12px;
    selection-background-color: {COLORS['primary']};
    min-height: 20px;
}}

QLineEdit:focus, QComboBox:focus {{
    border: 1px solid {COLORS['primary']};
    background-color: {COLORS['bg_hover']};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid {COLORS['text_muted']};
    margin-right: 8px;
}}

QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text']};
    selection-background-color: {COLORS['primary']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 4px;
}}

/* ---------- Кнопки ---------- */
QPushButton {{
    background-color: {COLORS['primary']};
    color: white;
    border: none;
    border-radius: 8px;
    padding: 9px 18px;
    font-size: 10pt;
    font-weight: 600;
    min-height: 20px;
}}

QPushButton:hover {{
    background-color: {COLORS['primary_hover']};
}}

QPushButton:pressed {{
    background-color: {COLORS['primary_press']};
}}

QPushButton#Secondary {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
}}

QPushButton#Secondary:hover {{
    background-color: {COLORS['bg_hover']};
    border: 1px solid {COLORS['primary']};
}}

/* ---------- Результаты (QTextEdit) ---------- */
QTextEdit {{
    background-color: {COLORS['bg_input']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 10px;
    font-family: "Consolas", "JetBrains Mono", "Courier New";
    font-size: 10pt;
    selection-background-color: {COLORS['primary']};
}}

/* ---------- Таблица ---------- */
QTableWidget {{
    background-color: {COLORS['bg_input']};
    alternate-background-color: {COLORS['bg_card']};
    color: {COLORS['text']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    gridline-color: {COLORS['border']};
    selection-background-color: {COLORS['primary']};
    font-size: 9.5pt;
}}

QHeaderView::section {{
    background-color: {COLORS['header_grad1']};
    color: {COLORS['text']};
    padding: 8px;
    border: none;
    border-right: 1px solid {COLORS['border']};
    border-bottom: 1px solid {COLORS['border']};
    font-weight: 600;
    font-size: 9.5pt;
}}

QTableWidget::item {{
    padding: 6px;
}}

QTableCornerButton::section {{
    background-color: {COLORS['header_grad1']};
    border: none;
}}

/* ---------- Скроллбары ---------- */
QScrollBar:vertical {{
    background: {COLORS['bg']};
    width: 10px;
    margin: 0;
}}

QScrollBar::handle:vertical {{
    background: {COLORS['border']};
    border-radius: 5px;
    min-height: 30px;
}}

QScrollBar::handle:vertical:hover {{
    background: {COLORS['primary']};
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}

QScrollBar:horizontal {{
    background: {COLORS['bg']};
    height: 10px;
}}

QScrollBar::handle:horizontal {{
    background: {COLORS['border']};
    border-radius: 5px;
    min-width: 30px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {COLORS['primary']};
}}

QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}

/* ---------- Заголовки секций ---------- */
#SectionTitle {{
    font-size: 11pt;
    font-weight: 700;
    color: {COLORS['text']};
    padding: 6px 0;
}}

#Hint {{
    color: {COLORS['text_muted']};
    font-size: 9pt;
}}
"""