from aqt import mw
from aqt.qt import *
from aqt import gui_hooks
from .addon import AnkiCramAddon

addon = AnkiCramAddon()
mw.ankicram_addon = addon

def add_menu_item():
    action = QAction("AnkiCram", mw)
    action.triggered.connect(addon.show_dialog)
    mw.form.menuTools.addAction(action)

gui_hooks.reviewer_did_answer_card.append(addon.on_answer_card)
gui_hooks.profile_did_open.append(add_menu_item)
