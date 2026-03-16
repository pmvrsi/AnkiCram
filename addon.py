from aqt import mw
from aqt.qt import *
from .widgets import CramCornerWidget
from .dialog import AnkiCramDialog
from .Changelog import ChangelogDialog
from .theme import VERSION


class AnkiCramAddon:
    def __init__(self, manager_name=None):
        self.manager_name = manager_name
        self.current_cram_did = None
        self.current_cram_name = None
        self.original_deck_id = None
        self.session_start_time = None
        self.session_cards_reviewed = 0
        self.session_cards_failed = 0
        self.session_reloops = 0
        self.infinite_loop_enabled = True
        self.persistent_deck_mode = False
        self.base_search = ""
        self.failed_cards = set()
        self.corner_widget = None

        QTimer.singleShot(1000, self.check_for_update)

    def is_active_session(self):
        return self.current_cram_did is not None

    def show_dialog(self):
        dialog = AnkiCramDialog(mw)
        dialog.exec()

    def show_changelog(self):
        dialog = ChangelogDialog(mw)
        dialog.exec()

    def check_for_update(self):
        if not self.manager_name:
            return
            
        config = mw.addonManager.getConfig(self.manager_name) or {}
        last_version = config.get("last_version", "v1.0.0")
        
        if last_version != VERSION:
            self.show_changelog()
            config["last_version"] = VERSION
            mw.addonManager.writeConfig(self.manager_name, config)

    def show_corner_widget(self):
        if not self.corner_widget:
            self.corner_widget = CramCornerWidget(mw)
        self.corner_widget.show()
        self.corner_widget.update_position()

    def hide_corner_widget(self):
        if self.corner_widget:
            self.corner_widget.hide()

    def on_answer_card(self, reviewer, card, ease):
        if not self.is_active_session():
            return

        target_did = self.current_cram_did
        if card.did != target_did and card.odid != target_did:
            return

        self.session_cards_reviewed += 1

        try:
            ease_int = int(ease)
        except (ValueError, TypeError):
            return

        if ease_int == 1:
            self.session_cards_failed += 1
            if self.infinite_loop_enabled:
                self.failed_cards.add(card.id)
        else:
            self.failed_cards.discard(card.id)


