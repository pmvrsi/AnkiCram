from aqt.qt import *
from .theme import THEME, VERSION
from .widgets import RoundedWidget, RoundedButton


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(420, 540)
        self.setup_ui()
        self._drag_pos = None

    def setup_ui(self):
        container = RoundedWidget(
            bg_color=THEME['bg'],
            border_color=THEME['glass_border'],
            radius=16,
            parent=self
        )
        container.setObjectName("AboutContainer")
        container.setStyleSheet(f"""
            QWidget#AboutContainer {{
                background-color: transparent;
                border: none;
                border-radius: 20px;
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        close_btn = RoundedButton(
            text="✕",
            radius=14,
            bg_color=THEME['glass'],
            hover_color=THEME['primary'],
            text_color=THEME['text_muted'],
            hover_text_color="white",
            parent=self
        )
        close_btn.setFixedSize(28, 28)
        close_font = QFont("Inter")
        close_font.setPixelSize(18)
        close_btn.setFont(close_font)
        close_btn.clicked.connect(self.accept)

        close_container = QHBoxLayout()
        close_container.addStretch()
        close_container.addWidget(close_btn)
        layout.addLayout(close_container)

        layout.addSpacing(10)

        logo = QLabel()
        logo.setText(f"<span style='font-size:36px; font-weight:800; color:{THEME['text']};'>Anki</span><span style='font-size:36px; font-weight:800; color:{THEME['primary']};'>Cram.</span>")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(logo)

        layout.addSpacing(8)

        credit = QLabel()
        credit.setTextFormat(Qt.TextFormat.RichText)
        credit.setOpenExternalLinks(True)
        credit.setText(f"Project by <a href='https://paramveer.co.uk' style='font-family: \"EB Garamond\", Georgia, serif; color: {THEME['primary']}; text-decoration: none;'><i>Paramveer.</i></a>")
        credit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit.setStyleSheet(f"""
            font-size: 13px;
            color: {THEME['text_muted']};
            border: none;
            background: transparent;
        """)
        layout.addWidget(credit)

        layout.addSpacing(20)

        version_lbl = QLabel(f"Version {VERSION}")
        version_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_lbl.setStyleSheet(f"""
            font-size: 12px;
            font-weight: 600;
            color: {THEME['text']};
            border: none;
            background: transparent;
        """)
        layout.addWidget(version_lbl)

        layout.addSpacing(15)

        desc_text = QLabel("An Anki add-on that lets you loop and rebuild\ndecks infinitely without ruining your\nlong-term spaced repetition data.")
        desc_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_text.setWordWrap(True)
        desc_text.setStyleSheet(f"""
            font-size: 12px;
            color: {THEME['text_muted']};
            line-height: 1.4;
            border: none;
            background: transparent;
        """)
        layout.addWidget(desc_text)

        layout.addSpacing(25)

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet(f"background: {THEME['glass_border']}; border: none; max-height: 1px;")
        layout.addWidget(divider)

        layout.addSpacing(20)

        license_title = QLabel("Open Source Licence")
        license_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        license_title.setStyleSheet(f"""
            font-size: 11px;
            font-weight: 700;
            color: {THEME['text_muted']};
            letter-spacing: 1px;
            text-transform: uppercase;
            border: none;
            background: transparent;
        """)
        layout.addWidget(license_title)

        layout.addSpacing(8)

        license_text = QLabel("This project is open source under the MIT Licence.\nFree to use, modify, and distribute.")
        license_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        license_text.setWordWrap(True)
        license_text.setStyleSheet(f"""
            font-size: 12px;
            color: {THEME['text_muted']};
            line-height: 1.5;
            border: none;
            background: transparent;
        """)
        layout.addWidget(license_text)

        layout.addSpacing(20)

        divider2 = QFrame()
        divider2.setFrameShape(QFrame.Shape.HLine)
        divider2.setStyleSheet(f"background: {THEME['glass_border']}; border: none; max-height: 1px;")
        layout.addWidget(divider2)

        layout.addSpacing(20)

        github_btn = RoundedButton(
            text="GitHub",
            radius=20,
            bg_color="transparent",
            hover_color=THEME['glass_hover'],
            text_color=THEME['text'],
            border_color=THEME['glass_border'],
            border_width=1,
            parent=self
        )
        github_btn.setFixedHeight(44)
        github_btn.setFixedWidth(160)
        github_font = QFont("Inter")
        github_font.setPixelSize(14)
        github_font.setWeight(QFont.Weight.DemiBold)
        github_btn.setFont(github_font)
        github_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/pmvrsi/AnkiCram/")))

        github_container = QHBoxLayout()
        github_container.addStretch()
        github_container.addWidget(github_btn)
        github_container.addStretch()
        layout.addLayout(github_container)

        layout.addSpacing(12)

        changelog_btn = RoundedButton(
            text="Changelog",
            radius=20,
            bg_color="transparent",
            hover_color=THEME['glass_hover'],
            text_color=THEME['text'],
            border_color=THEME['glass_border'],
            border_width=1,
            parent=self
        )
        changelog_btn.setFixedHeight(44)
        changelog_btn.setFixedWidth(160)
        changelog_font = QFont("Inter")
        changelog_font.setPixelSize(14)
        changelog_font.setWeight(QFont.Weight.DemiBold)
        changelog_btn.setFont(changelog_font)
        changelog_btn.clicked.connect(self.show_changelog)

        changelog_container = QHBoxLayout()
        changelog_container.addStretch()
        changelog_container.addWidget(changelog_btn)
        changelog_container.addStretch()
        layout.addLayout(changelog_container)

        layout.addStretch()

    def show_changelog(self):
        from .Changelog import ChangelogDialog
        dialog = ChangelogDialog(self)
        dialog.exec()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if self._drag_pos:
            delta = event.globalPosition().toPoint() - self._drag_pos
            self.move(self.pos() + delta)
            self._drag_pos = event.globalPosition().toPoint()
            event.accept()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
