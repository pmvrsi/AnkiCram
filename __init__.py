import os
from aqt import mw
from aqt.qt import *
from aqt import gui_hooks

# Load bundled fonts so they work on all systems
_fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
if os.path.isdir(_fonts_dir):
    for _font_file in os.listdir(_fonts_dir):
        if _font_file.endswith((".ttf", ".otf")):
            QFontDatabase.addApplicationFont(os.path.join(_fonts_dir, _font_file))

from .addon import AnkiCramAddon

addon = AnkiCramAddon()
mw.ankicram_addon = addon

def add_menu_item():
    action = QAction("AnkiCram", mw)
    action.triggered.connect(addon.show_dialog)
    mw.form.menuTools.addAction(action)

gui_hooks.reviewer_did_answer_card.append(addon.on_answer_card)
gui_hooks.profile_did_open.append(add_menu_item)
