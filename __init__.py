import os
from aqt import mw, gui_hooks
from aqt.qt import *
from aqt.overview import Overview

_fonts_dir = os.path.join(os.path.dirname(__file__), "fonts")
if os.path.isdir(_fonts_dir):
    for _font_file in os.listdir(_fonts_dir):
        if _font_file.endswith((".ttf", ".otf")):
            QFontDatabase.addApplicationFont(os.path.join(_fonts_dir, _font_file))

from .addon import AnkiCramAddon

addon = AnkiCramAddon(__name__)
mw.ankicram_addon = addon

def add_menu_item():
    action = QAction("AnkiCram", mw)
    action.triggered.connect(addon.show_dialog)
    mw.form.menuTools.addAction(action)

def on_webview_will_set_content(web_content, context):
    if not isinstance(context, Overview):
        return
    
    try:
        current_deck_name = mw.col.decks.get_current()['name']
        if not current_deck_name.startswith("AnkiCram - "):
            return
    except Exception:
        return

    css = "button#options, button#rebuild, button#empty { display: none !important; }"
    web_content.head += f"<style>{css}</style>"

gui_hooks.reviewer_did_answer_card.append(addon.on_answer_card)
gui_hooks.profile_did_open.append(add_menu_item)
gui_hooks.webview_will_set_content.append(on_webview_will_set_content)
