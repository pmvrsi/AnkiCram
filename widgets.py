import sys
from aqt import mw
from aqt.qt import *
from .theme import THEME, css_to_qcolor


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class RoundedWidget(QWidget):

    def __init__(self, bg_color, border_color, radius, border_width=1, parent=None):
        super().__init__(parent)
        self._bg_color = QColor(bg_color)
        self._border_color = QColor(border_color)
        self._radius = radius
        self._border_width = border_width

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), self._radius, self._radius)
        painter.setClipPath(path)
        painter.fillPath(path, self._bg_color)
        if self._border_width > 0 and self._border_color.alpha() > 0:
            pen = QPen(self._border_color, self._border_width)
            painter.setPen(pen)
            painter.drawPath(path)
        painter.end()


class StatCard(QFrame):
    def __init__(self, icon, label, value, value_color=None):
        super().__init__()
        if value_color is None:
            value_color = THEME['text']

        self._bg_normal = css_to_qcolor(THEME['glass'])
        self._bg_hover_target = css_to_qcolor(THEME['glass_hover'])
        self._border_normal = css_to_qcolor(THEME['glass_border'])
        self._border_hover_target = css_to_qcolor(THEME['primary'])

        self._current_bg = self._bg_normal
        self._current_border = self._border_normal
        self._radius = 10

        self.ani = QVariantAnimation(self)
        self.ani.setDuration(250)
        self.ani.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.ani.valueChanged.connect(self._on_ani_value_changed)

        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setStyleSheet("background-color: transparent; border: none; border-radius: 16px;")
        
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

    def _on_ani_value_changed(self, value):
        self._current_bg = self._lerp_color(self._bg_normal, self._bg_hover_target, value)
        self._current_border = self._lerp_color(self._border_normal, self._border_hover_target, value)
        self.update()

    def _lerp_color(self, c1, c2, factor):
        r = c1.red() + (c2.red() - c1.red()) * factor
        g = c1.green() + (c2.green() - c1.green()) * factor
        b = c1.blue() + (c2.blue() - c1.blue()) * factor
        a = c1.alpha() + (c2.alpha() - c1.alpha()) * factor
        return QColor(int(r), int(g), int(b), int(a))

    def enterEvent(self, event):
        if sys.platform != "win32":
            self.ani.setDirection(QAbstractAnimation.Direction.Forward)
            if self.ani.state() != QAbstractAnimation.State.Running:
                self.ani.start()
        else:
            self._current_bg = self._bg_hover_target
            self._current_border = self._border_hover_target
            self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if sys.platform != "win32":
            self.ani.setDirection(QAbstractAnimation.Direction.Backward)
            if self.ani.state() != QAbstractAnimation.State.Running:
                self.ani.start()
        else:
            self._current_bg = self._bg_normal
            self._current_border = self._border_normal
            self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)
        
        painter.fillPath(path, self._current_bg)
        pen = QPen(self._current_border, 1)
        painter.setPen(pen)
        painter.drawPath(path)
        painter.end()


class DeckSelectButton(QPushButton):
    def __init__(self, name, deck_id, parent=None):
        super().__init__(parent)
        self.deck_name = name
        self.deck_id = deck_id
        self.setCheckable(True)
        self.setFixedHeight(60)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._radius = 8

        self._bg_normal = css_to_qcolor(THEME['glass'])
        self._bg_hover = css_to_qcolor(THEME['glass_hover'])
        self._bg_selected = css_to_qcolor("rgba(167, 139, 250, 0.15)")
        
        self._border_normal = css_to_qcolor(THEME['glass_border'])
        self._border_active = css_to_qcolor(THEME['primary'])

        self._current_bg = self._bg_normal
        self._current_border = self._border_normal

        self.ani = QVariantAnimation(self)
        self.ani.setDuration(200)
        self.ani.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.ani.valueChanged.connect(self._on_ani_value_changed)

        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
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

    def _on_ani_value_changed(self, value):
        target_bg = self._get_target_bg()
        target_border = self._get_target_border()
        
        self._current_bg = self._lerp_color(self._bg_normal if self.ani.direction() == QAbstractAnimation.Direction.Backward else self._current_bg, target_bg, value)
        self._current_border = self._lerp_color(self._border_normal if self.ani.direction() == QAbstractAnimation.Direction.Backward else self._current_border, target_border, value)
        self.update()

    def _get_target_bg(self):
        if self.isChecked(): return self._bg_selected
        if self.underMouse(): return self._bg_hover
        return self._bg_normal

    def _get_target_border(self):
        if self.isChecked() or self.underMouse(): return self._border_active
        return self._border_normal

    def _lerp_color(self, c1, c2, factor):
        r = c1.red() + (c2.red() - c1.red()) * factor
        g = c1.green() + (c2.green() - c1.green()) * factor
        b = c1.blue() + (c2.blue() - c1.blue()) * factor
        a = c1.alpha() + (c2.alpha() - c1.alpha()) * factor
        return QColor(int(r), int(g), int(b), int(a))

    def enterEvent(self, event):
        if sys.platform != "win32":
            self.ani.setDirection(QAbstractAnimation.Direction.Forward)
            self.ani.start()
        else:
            self.update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if sys.platform != "win32":
            self.ani.setDirection(QAbstractAnimation.Direction.Backward)
            self.ani.start()
        else:
            self.update_style()
        super().leaveEvent(event)

    def update_style(self):
        if not self.ani.state() == QAbstractAnimation.State.Running:
            self._current_bg = self._get_target_bg()
            self._current_border = self._get_target_border()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)
        
        painter.fillPath(path, self._current_bg)
        pen = QPen(self._current_border, 1)
        painter.setPen(pen)
        painter.drawPath(path)
        painter.end()


class RoundedButton(QPushButton):
    def __init__(self, text, radius, bg_color, hover_color, text_color="white", hover_text_color=None, border_color=None, border_width=0, gradient=None, parent=None):
        if text == "×":
            text = "✕"
            
        super().__init__(text, parent)
        self._radius = radius
        self._bg_color = css_to_qcolor(bg_color)
        self._hover_target_color = css_to_qcolor(hover_color)
        self._text_color = css_to_qcolor(text_color)
        self._hover_text_target = css_to_qcolor(hover_text_color) if hover_text_color else self._text_color
        self._border_color = css_to_qcolor(border_color) if border_color else QColor(0, 0, 0, 0)
        self._border_width = border_width
        self._gradient_stops = gradient
        
        self._current_bg = self._bg_color
        self._current_text = self._text_color
        
        self.ani = QVariantAnimation(self)
        self.ani.setDuration(200)
        self.ani.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.ani.valueChanged.connect(self._on_ani_value_changed)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)
        self.setStyleSheet("border: none; background: transparent;")

    def _on_ani_value_changed(self, value):
        self._current_bg = self._lerp_color(self._bg_color, self._hover_target_color, value)
        self._current_text = self._lerp_color(self._text_color, self._hover_text_target, value)
        self.update()

    def _lerp_color(self, c1, c2, factor):
        r = c1.red() + (c2.red() - c1.red()) * factor
        g = c1.green() + (c2.green() - c1.green()) * factor
        b = c1.blue() + (c2.blue() - c1.blue()) * factor
        a = c1.alpha() + (c2.alpha() - c1.alpha()) * factor
        return QColor(int(r), int(g), int(b), int(a))

    def enterEvent(self, event):
        if sys.platform != "win32":
            self.ani.setDirection(QAbstractAnimation.Direction.Forward)
            if self.ani.state() != QAbstractAnimation.State.Running:
                self.ani.start()
        else:
            self._current_bg = self._hover_target_color
            self._current_text = self._hover_text_target
            self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        if sys.platform != "win32":
            self.ani.setDirection(QAbstractAnimation.Direction.Backward)
            if self.ani.state() != QAbstractAnimation.State.Running:
                self.ani.start()
        else:
            self._current_bg = self._bg_color
            self._current_text = self._text_color
            self.update()
        super().leaveEvent(event)

    def _get_bg_brush(self):
        if self.ani.state() == QAbstractAnimation.State.Running or self.underMouse():
            return QBrush(self._current_bg)
        
        if self._gradient_stops:
            grad = QLinearGradient(0, 0, self.width(), self.height())
            for pos, color in self._gradient_stops:
                grad.setColorAt(pos, css_to_qcolor(color))
            return QBrush(grad)
            
        return QBrush(self._bg_color)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)
        
        painter.fillPath(path, self._get_bg_brush())
        
        if self._border_width > 0:
            pen = QPen(self._border_color, self._border_width)
            painter.setPen(pen)
            painter.drawPath(path)
            
        painter.setPen(self._current_text)
        painter.setFont(self.font())
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, self.text())
        painter.end()


class CramCornerWidget(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(140, 50)
        self._bg = QColor(THEME['bg'])
        self._border = QColor(THEME['primary'])
        self._radius = 25
        self.setup_ui()
        self.update_position()
        self.clicked.connect(self.show_menu)

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel()
        self.label.setText(f"<span style='color:{THEME['text']}; font-weight:800;'>Anki</span><span style='color:{THEME['primary']}; font-weight:800;'>Cram.</span>")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("background: transparent; border: none; font-size: 18px; font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;")
        layout.addWidget(self.label)

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 25px;
            }}
            QPushButton:hover {{
                background-color: transparent;
            }}
        """)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._drag_position = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5)
        path = QPainterPath()
        path.addRoundedRect(rect, self._radius, self._radius)
        painter.setClipPath(path)
        painter.fillPath(path, self._bg)
        pen = QPen(self._border, 1)
        painter.setPen(pen)
        painter.drawPath(path)
        painter.end()

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
