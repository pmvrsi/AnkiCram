from aqt import mw
from aqt.qt import *
from .widgets import CramCornerWidget
from .dialog import AnkiCramDialog


class AnkiCramAddon:
    def __init__(self):
        self.current_cram_did = None
        self.current_cram_name = None
        self.original_deck_id = None
        self.session_start_time = None
        self.session_cards_reviewed = 0
        self.session_cards_failed = 0
        self.infinite_loop_enabled = True
        self.persistent_deck_mode = False
        self.base_search = ""
        self.failed_cards = set()
        self.corner_widget = None
        self._rebuild_timer = QTimer()
        self._rebuild_timer.setSingleShot(True)
        self._rebuild_timer.timeout.connect(self._do_delayed_rebuild)

    def is_active_session(self):
        return self.current_cram_did is not None

    def show_dialog(self):
        dialog = AnkiCramDialog(mw)
        dialog.exec()

    def show_corner_widget(self):
        if not self.corner_widget:
            self.corner_widget = CramCornerWidget(mw)
        self.corner_widget.show()
        self.corner_widget.update_position()

    def hide_corner_widget(self):
        if self.corner_widget:
            self.corner_widget.hide()

    def rebuild_filtered_deck(self):
        if not self.is_active_session():
            return
        self._rebuild_timer.start(200)

    def _do_delayed_rebuild(self):
        try:
            if self.is_active_session():
                mw.col.sched.rebuild_filtered_deck(self.current_cram_did)
        except Exception:
            pass

    def on_answer_card(self, reviewer, card, ease):
        if not self.is_active_session():
            return
        if card.did != self.current_cram_did:
            return

        self.session_cards_reviewed += 1

        if ease == 1:
            self.session_cards_failed += 1
            if self.infinite_loop_enabled:
                self.failed_cards.add(card.id)
                self.rebuild_filtered_deck()
        else:
            self.failed_cards.discard(card.id)
