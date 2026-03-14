import time
from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo
from .theme import THEME, STYLESHEET
from .widgets import ClickableLabel, StatCard, DeckSelectButton, RoundedWidget, RoundedButton
from .About import AboutDialog


class AnkiCramDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(650)
        self.setMinimumHeight(600)

        self.deck_buttons = []
        self.tag_input = None
        self.infinite_loop_check = None
        self.persistent_deck_check = None

        self.central = RoundedWidget(
            bg_color=THEME['bg'],
            border_color=THEME['glass_border'],
            radius=24,
            parent=self
        )
        self.central.setObjectName("CentralWidget")
        self.central.setStyleSheet(f"""
            QWidget#CentralWidget {{
                background-color: transparent;
                border: none;
                border-radius: 24px;
            }}
        """ + STYLESHEET)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.central)

        self.layout = QVBoxLayout(self.central)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.setup_header()

        self.content_widget = QWidget()
        self.content_widget.setStyleSheet("background: transparent; border: none;")
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(40, 30, 40, 30)
        self.content_layout.setSpacing(25)
        self.content_widget.setLayout(self.content_layout)
        self.layout.addWidget(self.content_widget)

        self.setup_body()
        self._drag_pos = None

    def setup_header(self):
        header = QFrame()
        header.setFixedHeight(100)
        header.setStyleSheet(f"background: transparent; border-bottom: 1px solid {THEME['glass_border']};")

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(40, 0, 40, 0)

        logo_container = QVBoxLayout()
        logo_container.setSpacing(4)
        logo_container.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        logo = QLabel()
        logo.setText(f"<span style='font-size:24px; font-weight:800; color:{THEME['text']};'>Anki</span><span style='font-size:24px; font-weight:800; color:{THEME['primary']};'>Cram.</span>")
        logo.setStyleSheet("border: none; background: transparent;")

        credit_container = QHBoxLayout()
        credit_container.setSpacing(6)
        credit_container.setContentsMargins(0, 0, 0, 0)

        credit = QLabel()
        credit.setTextFormat(Qt.TextFormat.RichText)
        credit.setText("Project by <i style='font-family: \"EB Garamond\", Georgia, serif;'>Paramveer.</i>")
        credit.setStyleSheet(f"""
            font-size: 11px; 
            font-weight: 500; 
            font-family: 'Inter', 'Segoe UI', 'Helvetica Neue', sans-serif;
            color: {THEME['text_muted']}; 
            border: none; 
            background: transparent;
        """)

        info_icon = ClickableLabel("ⓘ")
        info_icon.setStyleSheet(f"""
            font-size: 13px; 
            color: {THEME['text_muted']}; 
            border: none; 
            background: transparent;
        """)
        info_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        info_icon.clicked.connect(self.show_about_dialog)

        credit_container.addWidget(credit)
        credit_container.addWidget(info_icon)
        credit_container.addStretch()

        credit_wrapper = QWidget()
        credit_wrapper.setLayout(credit_container)
        credit_wrapper.setStyleSheet("background: transparent; border: none;")

        logo_container.addWidget(logo)
        logo_container.addWidget(credit_wrapper)

        h_layout.addLayout(logo_container)

        close_btn = RoundedButton(
            text="✕",
            radius=14,
            bg_color=THEME['glass'],
            hover_color=THEME['primary'],
            text_color=THEME['text_muted'],
            hover_text_color="white",
            parent=self
        )
        close_btn.setFixedSize(36, 36)
        close_font = QFont("Inter")
        close_font.setPixelSize(20)
        close_btn.setFont(close_font)
        close_btn.clicked.connect(self.reject)
        h_layout.addWidget(close_btn)

        header.setLayout(h_layout)
        self.layout.addWidget(header)

    def setup_body(self):
        while self.content_layout.count():
            item = self.content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

        active_cram = self.get_active_cram_deck()
        if active_cram:
            self.setup_active_session_ui(active_cram)
        else:
            self.setup_deck_selection_ui()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def setup_deck_selection_ui(self):
        lbl = QLabel("Select a deck to cram")
        lbl.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {THEME['text']}; border: none;")
        self.content_layout.addWidget(lbl)

        search_input = QLineEdit()
        search_input.setPlaceholderText("🔍 Search decks...")
        search_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 12px 16px;
                border: 1px solid {THEME['glass_border']};
                border-radius: 12px;
                background: {THEME['glass']};
                color: {THEME['text']};
                font-size: 14px;
            }}
            QLineEdit:focus {{ 
                border: 1px solid {THEME['primary']}; 
                background: {THEME['glass_hover']};
            }}
        """)
        search_input.textChanged.connect(self.filter_decks)
        self.content_layout.addWidget(search_input)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.deck_container = QWidget()
        self.deck_container.setStyleSheet("background: transparent;")
        self.deck_layout = QVBoxLayout()
        self.deck_layout.setSpacing(10)
        self.deck_layout.setContentsMargins(0, 0, 10, 0)
        self.deck_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.deck_container.setLayout(self.deck_layout)
        scroll.setWidget(self.deck_container)

        self.deck_buttons = []
        try:
            for deck in mw.col.decks.all_names_and_ids():
                if not deck.name.startswith("AnkiCram - ") and not self._is_filtered_deck(deck.id):
                    btn = DeckSelectButton(deck.name, deck.id)
                    btn.clicked.connect(lambda checked, b=btn: self.handle_deck_selection(b))
                    self.deck_layout.addWidget(btn)
                    self.deck_buttons.append(btn)
        except Exception as e:
            error_lbl = QLabel(f"Error loading decks: {str(e)}")
            error_lbl.setStyleSheet(f"color: {THEME['danger']}; border: none;")
            self.deck_layout.addWidget(error_lbl)

        if self.deck_buttons:
            self.deck_buttons[0].setChecked(True)
            self.deck_buttons[0].update_style()

        self.content_layout.addWidget(scroll, 1)

        settings_frame = QFrame()
        settings_frame.setStyleSheet(f"background: {THEME['glass']}; border: 1px solid {THEME['glass_border']}; border-radius: 10px;")
        settings_layout = QVBoxLayout()
        settings_layout.setContentsMargins(20, 20, 20, 20)

        opt_row = QHBoxLayout()
        self.infinite_loop_check = QCheckBox("Infinite Loop (Retry fails instantly)")
        self.infinite_loop_check.setChecked(True)
        self.persistent_deck_check = QCheckBox("Keep deck after session")
        opt_row.addWidget(self.infinite_loop_check)
        opt_row.addSpacing(20)
        opt_row.addWidget(self.persistent_deck_check)
        opt_row.addStretch()
        settings_layout.addLayout(opt_row)

        tag_row = QHBoxLayout()
        tag_icon = QLabel("🏷️")
        tag_icon.setStyleSheet("border: none; font-size: 16px;")
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Filter by tags (e.g. 'important')...")
        tag_row.addWidget(tag_icon)
        tag_row.addWidget(self.tag_input)
        settings_layout.addLayout(tag_row)

        settings_frame.setLayout(settings_layout)
        self.content_layout.addWidget(settings_frame)

        self.start_btn = RoundedButton(
            text="Start Cram Session",
            radius=27,
            bg_color="#a78bfa",
            hover_color="#6366f1",
            text_color="white",
            border_color="rgba(255, 255, 255, 0.2)",
            border_width=1,
            gradient=[(0, "#a78bfa"), (1, "#6366f1")],
            parent=self
        )
        self.start_btn.setFixedHeight(55)
        start_font = QFont("Inter")
        start_font.setPixelSize(16)
        start_font.setWeight(QFont.Weight.Bold)
        self.start_btn.setFont(start_font)
        self.start_btn.clicked.connect(self.start_cramming)

        btn_shadow = QGraphicsDropShadowEffect(self.start_btn)
        btn_shadow.setBlurRadius(25)
        btn_shadow.setColor(QColor(167, 139, 250, 80))
        btn_shadow.setOffset(0, 8)
        self.start_btn.setGraphicsEffect(btn_shadow)
        self.content_layout.addWidget(self.start_btn)

    def setup_active_session_ui(self, active_cram):
        addon = mw.ankicram_addon

        info_frame = QFrame()
        info_frame.setStyleSheet(f"background: rgba(167, 139, 250, 0.1); border-radius: 10px; border: 1px solid {THEME['primary']};")
        info_layout = QVBoxLayout()
        info_layout.setContentsMargins(20, 20, 20, 20)

        status_lbl = QLabel("CURRENTLY CRAMMING")
        status_lbl.setStyleSheet(f"font-size: 11px; font-weight: 700; color: {THEME['primary']}; letter-spacing: 1px; border: none; background: transparent;")
        deck_lbl = QLabel(active_cram['original_name'])
        deck_lbl.setStyleSheet(f"font-size: 22px; font-weight: 700; color: white; margin-top: 5px; border: none; background: transparent;")

        info_layout.addWidget(status_lbl)
        info_layout.addWidget(deck_lbl)
        info_frame.setLayout(info_layout)
        self.content_layout.addWidget(info_frame)

        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)

        elapsed = (time.time() - addon.session_start_time) / 60 if addon.session_start_time else 0
        retention = 0
        if addon.session_cards_reviewed > 0:
            retention = ((addon.session_cards_reviewed - addon.session_cards_failed) / addon.session_cards_reviewed) * 100

        stats_grid.addWidget(StatCard("⏱️", "Time", f"{elapsed:.0f}m"), 0, 0)
        stats_grid.addWidget(StatCard("✅", "Reviews", str(addon.session_cards_reviewed)), 0, 1)
        stats_grid.addWidget(StatCard("🧠", "Retention", f"{retention:.0f}%", THEME['secondary']), 1, 0)
        stats_grid.addWidget(StatCard("🔄", "Re-Loops", str(addon.session_reloops), THEME['primary']), 1, 1)

        self.content_layout.addLayout(stats_grid)
        self.content_layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        rebuild_btn = RoundedButton(
            text="Rebuild Deck",
            radius=25,
            bg_color="transparent",
            hover_color=THEME['glass_hover'],
            text_color=THEME['text'],
            border_color=THEME['glass_border'],
            border_width=1
        )
        rebuild_btn.setFixedHeight(50)
        rebuild_font = QFont("Inter")
        rebuild_font.setPixelSize(13)
        rebuild_font.setWeight(QFont.Weight.DemiBold)
        rebuild_btn.setFont(rebuild_font)
        rebuild_btn.clicked.connect(self.rebuild_deck)

        stop_btn = RoundedButton(
            text="End Session",
            radius=25,
            bg_color=THEME['danger_bg'],
            hover_color=THEME['danger'],
            text_color=THEME['danger'],
            hover_text_color="white",
            border_color="rgba(239, 68, 68, 0.3)",
            border_width=1
        )
        stop_btn.setFixedHeight(50)
        stop_font = QFont("Inter")
        stop_font.setPixelSize(13)
        stop_font.setWeight(QFont.Weight.DemiBold)
        stop_btn.setFont(stop_font)
        stop_btn.clicked.connect(self.stop_cramming)

        btn_layout.addWidget(rebuild_btn)
        btn_layout.addWidget(stop_btn)
        self.content_layout.addLayout(btn_layout)

    def show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def handle_deck_selection(self, clicked_btn):
        if not self.deck_buttons:
            return
        for btn in self.deck_buttons:
            if btn != clicked_btn:
                btn.setChecked(False)
                btn.update_style()
        clicked_btn.setChecked(True)
        clicked_btn.update_style()

    def filter_decks(self, search_text):
        if not self.deck_buttons:
            return
        search_text = search_text.lower()
        for btn in self.deck_buttons:
            if search_text in btn.deck_name.lower():
                btn.show()
            else:
                btn.hide()

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

    def _is_filtered_deck(self, deck_id):
        try:
            if hasattr(mw.col.decks, 'is_filtered'):
                return mw.col.decks.is_filtered(deck_id)
            deck = mw.col.decks.get(deck_id)
            if deck:
                return deck.get('dyn', 0) != 0
            return False
        except Exception:
            return False

    def get_active_cram_deck(self):
        for deck in mw.col.decks.all_names_and_ids():
            if deck.name.startswith("AnkiCram - "):
                return {
                    "id": deck.id,
                    "name": deck.name,
                    "original_name": deck.name.replace("AnkiCram - ", "", 1)
                }
        return None

    def rebuild_deck(self):
        try:
            addon = mw.ankicram_addon
            if not addon.is_active_session():
                tooltip("⚠️ No active session", period=1500)
                return

            original_did = addon.original_deck_id
            if not original_did:
                tooltip("⚠️ Original deck not found", period=1500)
                return

            cram_cards = mw.col.db.list(
                "SELECT id FROM cards WHERE did = ?", addon.current_cram_did
            )
            for cid in cram_cards:
                try:
                    card = mw.col.get_card(cid)
                    if card.odid != 0:
                        card.did = card.odid
                        card.odid = 0
                        card.odue = 0
                        mw.col.update_card(card)
                except Exception:
                    pass

            original_deck = mw.col.decks.get(original_did)
            if not original_deck:
                tooltip("⚠️ Original deck not found", period=1500)
                return
            deck_name = original_deck['name']

            deck_ids = [original_did]
            for d in mw.col.decks.all_names_and_ids():
                if d.name.startswith(deck_name + "::"):
                    deck_ids.append(d.id)

            all_cards = []
            for did in deck_ids:
                deck_cards = mw.col.db.list(
                    "SELECT id FROM cards WHERE did = ?", did
                )
                all_cards.extend(deck_cards)

            cards_moved = 0
            for cid in all_cards:
                try:
                    card = mw.col.get_card(cid)
                    if card.odid != 0 or card.queue == -1:
                        continue
                    card.odid = card.did
                    card.odue = card.due
                    card.did = addon.current_cram_did
                    card.due = -1
                    card.queue = 1
                    mw.col.update_card(card)
                    cards_moved += 1
                except Exception:
                    pass

            tooltip(f"✅ Deck rebuilt! ({cards_moved} cards)", period=2000)
            mw.reset()
            self.accept()
        except Exception as e:
            showInfo(f"Rebuild Error: {str(e)}")

    def start_cramming(self):
        try:
            selected_btn = next((b for b in self.deck_buttons if b.isChecked()), None)
            if not selected_btn:
                tooltip("⚠️ Please select a deck first", period=1800)
                return

            deck_name = selected_btn.deck_name
            deck_id = selected_btn.deck_id
            cram_name = f"AnkiCram - {deck_name}"

            existing_id = mw.col.decks.id_for_name(cram_name)
            if existing_id:
                try:
                    mw.col.sched.empty_filtered_deck(existing_id)
                    mw.col.decks.remove([existing_id])
                except Exception:
                    pass

            all_cards = []
            deck_ids = [deck_id]
            for d in mw.col.decks.all_names_and_ids():
                if d.name.startswith(deck_name + "::"):
                    deck_ids.append(d.id)

            for did in deck_ids:
                deck_cards = mw.col.db.list(
                    "SELECT id FROM cards WHERE did = ?", did
                )
                all_cards.extend(deck_cards)

            tag_filter = self.tag_input.text().strip() if self.tag_input else ""
            if tag_filter and all_cards:
                tags = [t.strip().lower() for t in tag_filter.split(",") if t.strip()]
                if tags:
                    filtered_cards = []
                    for cid in all_cards:
                        card = mw.col.get_card(cid)
                        note = card.note()
                        card_tags = [t.lower() for t in note.tags]
                        if any(tag in card_tags for tag in tags):
                            filtered_cards.append(cid)
                    all_cards = filtered_cards

            if not all_cards:
                tooltip("⚠️ No cards found in this deck", period=3000)
                return

            cram_did = mw.col.decks.new_filtered(cram_name)
            deck_obj = mw.col.decks.get(cram_did)
            deck_obj["terms"] = [["deck:_*_nonexistent_*_", 9999, 5]]
            deck_obj["resched"] = False
            deck_obj["previewDelay"] = 0
            mw.col.decks.save(deck_obj)

            cards_moved = 0
            for cid in all_cards:
                try:
                    card = mw.col.get_card(cid)
                    if card.odid != 0:
                        continue
                    if card.queue == -1:
                        continue
                    card.odid = card.did
                    card.odue = card.due
                    card.did = cram_did
                    card.due = -1
                    card.queue = 1
                    mw.col.update_card(card)
                    cards_moved += 1
                except Exception:
                    pass

            if cards_moved == 0:
                mw.col.decks.remove([cram_did])
                showInfo(
                    f"Could not move any cards to cram deck.\n\n"
                    f"Found {len(all_cards)} cards but none could be moved.\n\n"
                    f"Cards may already be in another filtered deck."
                )
                return

            addon = mw.ankicram_addon
            addon.original_deck_id = deck_id
            addon.session_start_time = time.time()
            addon.session_cards_reviewed = 0
            addon.session_cards_failed = 0
            addon.infinite_loop_enabled = self.infinite_loop_check.isChecked() if self.infinite_loop_check else True
            addon.persistent_deck_mode = self.persistent_deck_check.isChecked() if self.persistent_deck_check else False
            addon.current_cram_did = cram_did
            addon.current_cram_name = cram_name
            addon.base_search = f'deck:"{deck_name}"'
            addon.failed_cards = set()

            mw.col.decks.select(cram_did)
            mw.reset()
            addon.show_corner_widget()
            self.accept()
            tooltip(f"🚀 Cram started ({cards_moved} cards)", period=2500)

        except Exception as e:
            import traceback
            showInfo(f"Start Error:\n{str(e)}\n\nDetails:\n{traceback.format_exc()}")

    def stop_cramming(self):
        try:
            active = self.get_active_cram_deck()
            if not active:
                tooltip("⚠️ No active session", period=1500)
                return

            addon = mw.ankicram_addon
            cram_deck_id = active['id']

            mw.col.decks.select(1)

            if hasattr(mw, 'reviewer') and mw.reviewer:
                try:
                    mw.reviewer.cleanup()
                except Exception:
                    pass

            cleanup_success = False
            if not addon.persistent_deck_mode:
                try:
                    mw.col.sched.empty_filtered_deck(cram_deck_id)
                    mw.col.decks.remove([cram_deck_id])
                    cleanup_success = True
                except Exception:
                    try:
                        card_ids = mw.col.find_cards(f'deck:"{active["name"]}"')
                        for cid in card_ids:
                            card = mw.col.get_card(cid)
                            card.did = card.odid if card.odid else 1
                            card.odid = 0
                            mw.col.update_card(card)
                        mw.col.decks.remove([cram_deck_id])
                        cleanup_success = True
                    except Exception:
                        try:
                            mw.col.sched.empty_filtered_deck(cram_deck_id)
                            tooltip("⚠️ Deck emptied but not deleted. Remove manually if needed.", period=3000)
                        except Exception:
                            tooltip("⚠️ Please manually delete the cram deck", period=3000)

            addon.current_cram_did = None
            addon.current_cram_name = None
            addon.session_start_time = None
            addon.failed_cards = set()
            addon.session_cards_reviewed = 0
            addon.session_cards_failed = 0

            addon.hide_corner_widget()
            mw.reset()
            self.accept()

            if cleanup_success or addon.persistent_deck_mode:
                tooltip("✅ Session ended", period=2000)

        except Exception as e:
            addon = mw.ankicram_addon
            addon.current_cram_did = None
            addon.current_cram_name = None
            addon.failed_cards = set()
            addon.session_cards_reviewed = 0
            addon.session_cards_failed = 0
            addon.session_reloops = 0
            addon.session_start_time = time.time()
            addon.hide_corner_widget()

            showInfo(f"Session ended with errors: {str(e)}\n\nYou may need to manually delete the AnkiCram deck.")
            self.accept()
