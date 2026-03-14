from aqt.qt import *
from .theme import THEME, VERSION
from .widgets import RoundedWidget, RoundedButton

class ChangelogDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(480, 560)
        self.setup_ui()
        self._drag_pos = None

    def setup_ui(self):
        container = RoundedWidget(
            bg_color=THEME['bg'],
            border_color=THEME['glass_border'],
            radius=16,
            parent=self
        )
        container.setObjectName("ChangelogContainer")
        container.setStyleSheet(f"""
            QWidget#ChangelogContainer {{
                background-color: transparent;
                border: none;
                border-radius: 24px;
            }}
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(40, 35, 40, 35)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        close_container = QHBoxLayout()
        close_container.addStretch()
        close_btn = RoundedButton(
            text="✕",
            radius=16,
            bg_color=THEME['glass'],
            hover_color=THEME['primary'],
            text_color=THEME['text_muted'],
            hover_text_color="white",
            parent=self
        )
        close_btn.setFixedSize(32, 32)
        close_font = QFont("Inter")
        close_font.setPixelSize(18)
        close_btn.setFont(close_font)
        close_btn.clicked.connect(self.accept)
        close_container.addWidget(close_btn)
        layout.addLayout(close_container)

        logo = QLabel()
        logo.setText(f"<span style='font-size:32px; font-weight:800; color:{THEME['text']};'>Anki</span><span style='font-size:32px; font-weight:800; color:{THEME['primary']};'>Cram.</span>")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("border: none; background: transparent;")
        layout.addWidget(logo)

        credit = QLabel()
        credit.setTextFormat(Qt.TextFormat.RichText)
        credit.setText("Project by <i style='font-family: \"EB Garamond\", Georgia, serif;'>Paramveer.</i>")
        credit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        credit.setStyleSheet(f"font-size: 13px; color: {THEME['text_muted']}; border: none; background: transparent;")
        layout.addWidget(credit)
        
        layout.addSpacing(30)

        whats_new = QLabel("What's New")
        whats_new.setAlignment(Qt.AlignmentFlag.AlignCenter)
        whats_new.setStyleSheet(f"font-size: 24px; font-weight: 800; color: {THEME['text']}; border: none; background: transparent;")
        layout.addWidget(whats_new)

        ver_lbl = QLabel(f"{VERSION} Changelog")
        ver_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver_lbl.setStyleSheet(f"font-size: 12px; font-weight: 700; color: {THEME['primary']}; text-transform: uppercase; letter-spacing: 1px; border: none; background: transparent;")
        layout.addWidget(ver_lbl)

        layout.addSpacing(30)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet(f"""
            QScrollArea {{ 
                background: transparent; 
                border: none; 
            }}
            QScrollBar:vertical {{
                border: none;
                background: transparent;
                width: 4px;
                margin: 0px;
            }}
            QScrollBar::handle:vertical {{
                background: {THEME['glass_border']};
                min-height: 20px;
                border-radius: 2px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                border: none;
                background: none;
                height: 0px;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """)
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(0, 0, 15, 0)

        changes = [
            ("Windows UI Fix", "UI has been fixed where it was boxy and unrounded. Now it's rounded on Windows, matching the macOS version."),
            ("Imported Fonts", "Premium Inter and Garamond fonts are now imported directly with the extension for a consistent look on all systems."),
            ("Accurate Retention", "Fixed session stats. The retention percentage now correctly tracks your 'Again' answers."),
            ("Re-Loop Tracking", "Fixed the Re-Loops counter to correctly show how many times the deck has been rebuilt."),
        ]

        for title, desc in changes:
            text_layout = QVBoxLayout()
            t_lbl = QLabel(title)
            t_lbl.setStyleSheet(f"font-size: 14px; font-weight: 700; color: {THEME['text']}; border: none;")
            d_lbl = QLabel(desc)
            d_lbl.setWordWrap(True)
            d_lbl.setStyleSheet(f"font-size: 13px; color: {THEME['text_muted']}; border: none; line-height: 1.4;")
            
            text_layout.addWidget(t_lbl)
            text_layout.addWidget(d_lbl)
            content_layout.addLayout(text_layout)

        scroll.setWidget(content)
        layout.addWidget(scroll)
        
        layout.addSpacing(25)
        
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
        github_btn.setFixedWidth(180)
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
