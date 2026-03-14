from aqt import mw
from aqt.qt import *
from .theme import THEME


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class StatCard(QFrame):
    def __init__(self, icon, label, value, value_color=None):
        super().__init__()
        if value_color is None:
            value_color = THEME['text']

        self.setStyleSheet(f"""
            QFrame {{
                background-color: {THEME['glass']};
                border-radius: 16px;
                border: 1px solid {THEME['glass_border']};
            }}
            QFrame:hover {{
                border: 1px solid {THEME['primary']};
                background-color: {THEME['glass_hover']};
            }}
        """)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        top_layout = QHBoxLayout()
        icon_lbl = QLabel(icon)
        icon_lbl.setStyleSheet("font-size: 18px; border: none; background: transparent;")

        title_lbl = QLabel(label)
        title_lbl.setStyleSheet(f"color: {THEME['text_muted']}; font-size: 12px; font-weight: 600; text-transform: uppercase; border: none; background: transparent;")

        top_layout.addWidget(icon_lbl)
        top_layout.addWidget(title_lbl)
        top_layout.addStretch()

        value_lbl = QLabel(str(value))
        value_lbl.setStyleSheet(f"color: {value_color}; font-size: 28px; font-weight: 800; border: none; background: transparent;")

        layout.addLayout(top_layout)
        layout.addSpacing(5)
        layout.addWidget(value_lbl)
        self.setLayout(layout)


class DeckSelectButton(QPushButton):
    def __init__(self, name, deck_id, parent=None):
        super().__init__(parent)
        self.deck_name = name
        self.deck_id = deck_id
        self.setCheckable(True)
        self.setFixedHeight(60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        display_name = name.split("::")[-1]
        path = "::".join(name.split("::")[:-1])
        self.setup_ui(display_name, path)

    def setup_ui(self, display_name, path):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 10, 20, 10)
        layout.setSpacing(2)

        if path:
            path_lbl = QLabel(path)
            path_lbl.setStyleSheet(f"font-size: 11px; color: {THEME['text_muted']}; background: transparent; border: none;")
            layout.addWidget(path_lbl)

        name_lbl = QLabel(display_name)
        name_lbl.setStyleSheet(f"font-size: 15px; font-weight: bold; color: {THEME['text']}; background: transparent; border: none;")
        layout.addWidget(name_lbl)

        self.setLayout(layout)
        self.update_style()
        self.toggled.connect(self.update_style)

    def update_style(self):
        if self.isChecked():
            border = THEME['primary']
            bg = "rgba(167, 139, 250, 0.15)"
        else:
            border = THEME['glass_border']
            bg = THEME['glass']

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 12px;
                text-align: left;
            }}
            QPushButton:hover {{
                border: 1px solid {THEME['primary']};
                background-color: {THEME['glass_hover']};
            }}
        """)


class CramCornerWidget(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(140, 50)
        self.setup_ui()
        self.update_position()
        self.clicked.connect(self.show_menu)

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel()
        self.label.setText(f"<span style='color:{THEME['text']}; font-weight:800;'>Anki</span><span style='color:{THEME['primary']}; font-weight:800;'>Cram.</span>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("background: transparent; border: none; font-size: 18px; font-family: 'Segoe UI', sans-serif;")
        layout.addWidget(self.label)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {THEME['bg']};
                border: 1px solid {THEME['primary']};
                border-radius: 25px;
            }}
            QPushButton:hover {{
                background-color: rgba(167, 139, 250, 0.2);
            }}
        """)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._drag_position = None

    def update_position(self):
        if mw and mw.isVisible():
            mw_pos = mw.geometry()
            x_pos = mw_pos.x() + 20
            y_pos = mw_pos.y() + mw_pos.height() - self.height() - 100
            self.move(x_pos, y_pos)

    def show_menu(self):
        if hasattr(mw, 'ankicram_addon'):
            mw.ankicram_addon.show_dialog()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_position:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()
        else:
            super().mouseMoveEvent(event)
