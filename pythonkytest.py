import tkinter as tk
from tkinter import ttk
import tkinter.font # Explicitly import tkinter.font
from tkinter.scrolledtext import ScrolledText # For the event logger

# --- Style Configuration (Monkeytype-inspired) ---
STYLE_CONFIG = {
    "window_bg": "#202224",
    "content_frame_bg": "#282a2e", # Slightly different for content area if needed
    "key_bg": "#3a3d42",
    "key_fg": "#d4d4d4",
    "key_pressed_bg": "#626569",
    "key_active_modifier_bg": "#4CAF50",
    "info_fg": "#d4d4d4",
    "text_widget_bg": "#2c2f33",
    "text_widget_fg": "#d4d4d4",
    "font_family": "Segoe UI",
    "font_size_normal": 9,
    "font_size_small": 8,
    "base_key_width": 5,
    "base_key_height": 2,
    "key_relief": tk.FLAT,
    "key_borderwidth": 2,
    "highlight_thickness": 0,
}
try:
    # Test if font exists
    _test_label = tk.Label(font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"]))
    _test_label.destroy()
except tk.TclError:
    STYLE_CONFIG["font_family"] = "Arial" # A common fallback

# --- Key Definitions Helper (KD) ---
def KD(label, keysyms, width=1.0, height=1.0, char_override=None, small_font=False):
    """Helper to create key definition dictionaries."""
    if isinstance(keysyms, str):
        keysyms = [keysyms]
    final_keysyms = set()
    # Add lowercase, uppercase for single alpha chars, and original keysyms
    for k_orig in keysyms:
        k = str(k_orig) # Ensure string for operations
        final_keysyms.add(k)
        if len(k) == 1 and k.isalpha():
            final_keysyms.add(k.lower())
            final_keysyms.add(k.upper())
        elif k.startswith("Cyrillic_") and len(k) == 10 and k[9].islower(): # e.g. Cyrillic_a
             final_keysyms.add("Cyrillic_" + k[9].upper()) # Add Cyrillic_A
        elif k.startswith("Cyrillic_") and len(k) == 10 and k[9].isupper(): # e.g. Cyrillic_A
             final_keysyms.add("Cyrillic_" + k[9].lower()) # Add Cyrillic_a

    # This auto-shifting for numbers/symbols is QWERTY-centric.
    # For other layouts, it's better to be explicit in the keysyms list.
    if len(label) == 1 and not any(str(ks).startswith("dead_") for ks in keysyms):
        if label.isdigit():
            shifted_map_qwerty = {'1':'exclam', '2':'at', '3':'numbersign', '4':'dollar', '5':'percent', '6':'asciicircum', '7':'ampersand', '8':'asterisk', '9':'parenleft', '0':'parenright'}
            if label in shifted_map_qwerty: final_keysyms.add(shifted_map_qwerty[label])
        elif not label.isalpha(): # Punctuation (QWERTY-centric)
            punct_map_qwerty = {'`': ['grave', 'asciitilde'], '-': ['minus', 'underscore'], '=': ['equal', 'plus'], '[': ['bracketleft', 'braceleft'], ']': ['bracketright', 'braceright'], '\\': ['backslash', 'bar'], ';': ['semicolon', 'colon'], "'": ['apostrophe', 'quotedbl'], ',': ['comma', 'less'], '.': ['period', 'greater'], '/': ['slash', 'question']}
            if label in punct_map_qwerty: final_keysyms.update(punct_map_qwerty[label])

    return {'label': label, 'keysyms': list(final_keysyms), 'char_override': char_override, 'width_factor': width, 'height_factor': height, 'small_font': small_font}

SPACER = "SPACER"

# --- Standard Peripheral Blocks (Can be reused by most layouts) ---
STD_F_KEYS_ROW = [
    [KD('Esc', 'Escape', width=1.4), SPACER, KD('F1', 'F1'), KD('F2', 'F2'), KD('F3', 'F3'), KD('F4', 'F4'), SPACER,
     KD('F5', 'F5'), KD('F6', 'F6'), KD('F7', 'F7'), KD('F8', 'F8'), SPACER,
     KD('F9', 'F9'), KD('F10', 'F10'), KD('F11', 'F11'), KD('F12', 'F12')]
]
STD_EDIT_BLOCK = [
    [KD('PrtSc', ['Print', 'Snapshot'], small_font=True, width=1.1), KD('ScrLk', 'Scroll_Lock', small_font=True, width=1.1), KD('Pause', 'Pause', small_font=True, width=1.1)]
]
STD_NAVIGATION_BLOCK = [
    [KD('Ins', 'Insert', small_font=True, width=1.1), KD('Home', 'Home', small_font=True, width=1.1), KD('PgUp', ['Prior', 'Page_Up'], small_font=True, width=1.1)],
    [KD('Del', 'Delete', small_font=True, width=1.1), KD('End', 'End', small_font=True, width=1.1), KD('PgDn', ['Next', 'Page_Down'], small_font=True, width=1.1)]
]
STD_ARROW_KEYS_BLOCK = [
    [SPACER, KD('↑', 'Up', width=1.1), SPACER],
    [KD('←', 'Left', width=1.1), KD('↓', 'Down', width=1.1), KD('→', 'Right', width=1.1)]
]
STD_NUMPAD_BLOCK_DOT_DECIMAL = [ # Numpad with . as decimal
    [KD('Num Lk', 'Num_Lock', small_font=True, width=1.1), KD(' / ', 'KP_Divide', width=1.1, char_override='/'), KD(' * ', 'KP_Multiply', width=1.1, char_override='*'), KD(' - ', 'KP_Subtract', width=1.1, char_override='-')],
    [KD('7', ['KP_7', 'KP_Home'], width=1.1), KD('8', ['KP_8', 'KP_Up'], width=1.1), KD('9', ['KP_9', 'KP_Prior'], width=1.1), KD(' + ', 'KP_Add', height=2.0, width=1.1, char_override='+')],
    [KD('4', ['KP_4', 'KP_Left'], width=1.1), KD('5', ['KP_5', 'KP_Begin'], width=1.1), KD('6', ['KP_6', 'KP_Right'], width=1.1)],
    [KD('1', ['KP_1', 'KP_End'], width=1.1), KD('2', ['KP_2', 'KP_Down'], width=1.1), KD('3', ['KP_3', 'KP_Next'], width=1.1), KD('Enter', 'KP_Enter', height=2.0, width=1.1, small_font=True)],
    [KD('0', ['KP_0', 'KP_Insert'], width=2.3), KD('.', ['KP_Decimal', 'KP_Delete'], width=1.1, char_override='.')]
]
STD_NUMPAD_BLOCK_COMMA_DECIMAL = [ # Numpad with , as decimal
    [KD('Num Lk', 'Num_Lock', small_font=True, width=1.1), KD(' / ', 'KP_Divide', width=1.1), KD(' * ', 'KP_Multiply', width=1.1), KD(' - ', 'KP_Subtract', width=1.1)],
    [KD('7', ['KP_7', 'KP_Home'], width=1.1), KD('8', ['KP_8', 'KP_Up'], width=1.1), KD('9', ['KP_9', 'KP_Prior'], width=1.1), KD(' + ', 'KP_Add', height=2.0, width=1.1)],
    [KD('4', ['KP_4', 'KP_Left'], width=1.1), KD('5', ['KP_5', 'KP_Begin'], width=1.1), KD('6', ['KP_6', 'KP_Right'], width=1.1)],
    [KD('1', ['KP_1', 'KP_End'], width=1.1), KD('2', ['KP_2', 'KP_Down'], width=1.1), KD('3', ['KP_3', 'KP_Next'], width=1.1), KD('Enter', 'KP_Enter', height=2.0, width=1.1, small_font=True)],
    [KD('0', ['KP_0', 'KP_Insert'], width=2.3), KD(',', ['KP_Separator', 'KP_Delete'], width=1.1, char_override=',')]]

# --- Layout Definitions (EXTENSIVE LIST) ---
LAYOUTS = {
    "QWERTY_Full_US": {
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('`', ['grave', 'asciitilde']), KD('1', ['1', 'exclam']), KD('2', ['2', 'at']), KD('3', ['3', 'numbersign']), KD('4', ['4', 'dollar']), KD('5', ['5', 'percent']), KD('6', ['6', 'asciicircum']), KD('7', ['7', 'ampersand']), KD('8', ['8', 'asterisk']), KD('9', ['9', 'parenleft']), KD('0', ['0', 'parenright']), KD('-', ['minus', 'underscore']), KD('=', ['equal', 'plus']), KD('Backspace', 'BackSpace', width=2.0, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('Q', 'Q'), KD('W', 'W'), KD('E', 'E'), KD('R', 'R'), KD('T', 'T'), KD('Y', 'Y'), KD('U', 'U'), KD('I', 'I'), KD('O', 'O'), KD('P', 'P'), KD('[', ['bracketleft', 'braceleft']), KD(']', ['bracketright', 'braceright']), KD('\\', ['backslash', 'bar'], width=1.5)],
            [KD('Caps Lock', 'Caps_Lock', width=1.8, small_font=True), KD('A', 'A'), KD('S', 'S'), KD('D', 'D'), KD('F', 'F'), KD('G', 'G'), KD('H', 'H'), KD('J', 'J'), KD('K', 'K'), KD('L', 'L'), KD(';', ['semicolon', 'colon']), KD("'", ['apostrophe', 'quotedbl']), KD('Enter', 'Return', width=2.2, small_font=True)],
            [KD('Shift', 'Shift_L', width=2.3, small_font=True), KD('Z', 'Z'), KD('X', 'X'), KD('C', 'C'), KD('V', 'V'), KD('B', 'B'), KD('N', 'N'), KD('M', 'M'), KD(',', ['comma', 'less']), KD('.', ['period', 'greater']), KD('/', ['slash', 'question']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_DOT_DECIMAL
    },
    "Spanish_ES_Full": {
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('º', ['masculine', 'ordfeminine', 'backslash']), KD('1', ['1', 'exclam', 'bar']), KD('2', ['2', 'quotedbl', 'at']), KD('3', ['3', 'periodcentered', 'numbersign', 'sterling']), KD('4', ['4', 'dollar', 'asciitilde']), KD('5', ['5', 'percent', 'EuroSign']), KD('6', ['6', 'ampersand', 'notsign']), KD('7', ['7', 'slash']), KD('8', ['8', 'parenleft']), KD('9', ['9', 'parenright']), KD('0', ['0', 'equal']), KD("'", ['apostrophe', 'question']), KD('¡', ['exclamdown', 'questiondown']), KD('Backspace', 'BackSpace', width=1.8, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('Q', 'Q'), KD('W', 'W'), KD('E', ['E', 'e', 'EuroSign']), KD('R', 'R'), KD('T', 'T'), KD('Y', 'Y'), KD('U', 'U'), KD('I', 'I'), KD('O', 'O'), KD('P', 'P'), KD('`', ['grave', 'dead_grave', 'asciicircum', 'dead_circumflex', 'bracketleft']), KD('+', ['plus', 'asterisk', 'bracketright', 'dead_tilde']), KD('Ç', ['ccedilla', 'Ccedilla', 'braceright'], width=1.2)],
            [KD('Caps Lock', 'Caps_Lock', width=1.7, small_font=True), KD('A', 'A'), KD('S', 'S'), KD('D', 'D'), KD('F', 'F'), KD('G', 'G'), KD('H', 'H'), KD('J', 'J'), KD('K', 'K'), KD('L', 'L'), KD('Ñ', ['ntilde', 'Ntilde']), KD('´', ['acute', 'dead_acute', 'diaeresis', 'dead_diaeresis', 'braceleft']), KD('Enter', 'Return', width=2.3, small_font=True)],
            [KD('Shift', 'Shift_L', width=1.2, small_font=True), KD('<', ['less', 'greater', 'bar']), KD('Z', 'Z'), KD('X', 'X'), KD('C', 'C'), KD('V', 'V'), KD('B', 'B'), KD('N', 'N'), KD('M', 'M'), KD(',', ['comma', 'semicolon']), KD('.', ['period', 'colon']), KD('-', ['minus', 'underscore']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_COMMA_DECIMAL
    },
    "German_DE_Full": { # QWERTZ
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('^', ['asciicircum', 'degree', 'dead_circumflex']), KD('1', ['1', 'exclam']), KD('2', ['2', 'quotedbl', 'twosuperior']), KD('3', ['3', 'section', 'threesuperior']), KD('4', ['4', 'dollar']), KD('5', ['5', 'percent']), KD('6', ['6', 'ampersand']), KD('7', ['7', 'slash', 'braceleft']), KD('8', ['8', 'parenleft', 'bracketleft']), KD('9', ['9', 'parenright', 'bracketright']), KD('0', ['0', 'equal', 'braceright']), KD('ß', ['ssharp', 'question', 'backslash']), KD('´', ['acute', 'grave', 'dead_acute', 'dead_grave']), KD('Backspace', 'BackSpace', width=1.8, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('Q', ['Q', 'q', 'at']), KD('W', 'W'), KD('E', ['E', 'e', 'EuroSign']), KD('R', 'R'), KD('T', 'T'), KD('Z', 'Z'), KD('U', 'U'), KD('I', 'I'), KD('O', 'O'), KD('P', 'P'), KD('Ü', ['udiaeresis', 'Udiaeresis']), KD('+', ['plus', 'asterisk', 'asciitilde']), KD('#', ['numbersign', 'apostrophe'], width=1.2)],
            [KD('Caps Lock', 'Caps_Lock', width=1.7, small_font=True), KD('A', 'A'), KD('S', 'S'), KD('D', 'D'), KD('F', 'F'), KD('G', 'G'), KD('H', 'H'), KD('J', 'J'), KD('K', 'K'), KD('L', 'L'), KD('Ö', ['odiaeresis', 'Odiaeresis']), KD('Ä', ['adiaeresis', 'Adiaeresis']), KD('Enter', 'Return', width=2.3, small_font=True)],
            [KD('Shift', 'Shift_L', width=1.2, small_font=True), KD('<', ['less', 'greater', 'bar', 'rightarrow']), KD('Y', 'Y'), KD('X', 'X'), KD('C', 'C'), KD('V', 'V'), KD('B', 'B'), KD('N', 'N'), KD('M', ['M', 'm', 'mu']), KD(',', ['comma', 'semicolon']), KD('.', ['period', 'colon']), KD('-', ['minus', 'underscore']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_COMMA_DECIMAL
    },
    "AZERTY_FR_Full": {
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('²', ['twosuperior', 'asciitilde']), KD('&', ['ampersand', '1']), KD('é', ['eacute', 'Eacute', '2', 'at']), KD('"', ['quotedbl', '3', 'numbersign']), KD("'", ['apostrophe', '4', 'braceleft']), KD('(', ['parenleft', '5', 'bracketleft']), KD('-', ['minus', '6', 'bar']), KD('è', ['egrave', 'Egrave', '7', 'grave']), KD('_', ['underscore', '8', 'backslash']), KD('ç', ['ccedilla', 'Ccedilla', '9', 'asciicircum']), KD('à', ['agrave', 'Agrave', '0', 'braceright']), KD(')', ['parenright', 'degree', 'bracketright']), KD('=', ['equal', 'plus', 'plusminus']), KD('Backspace', 'BackSpace', width=1.8, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('A', 'A'), KD('Z', 'Z'), KD('E', ['E', 'e', 'EuroSign']), KD('R', 'R'), KD('T', 'T'), KD('Y', 'Y'), KD('U', 'U'), KD('I', 'I'), KD('O', 'O'), KD('P', 'P'), KD('^', ['dead_circumflex', 'diaeresis', 'dead_diaeresis', '¨']), KD('$', ['dollar', 'sterling', 'currency']), KD('*', ['asterisk', 'mu', 'section'], width=1.2)],
            [KD('Caps Lock', 'Caps_Lock', width=1.7, small_font=True), KD('Q', 'Q'), KD('S', 'S'), KD('D', 'D'), KD('F', 'F'), KD('G', 'G'), KD('H', 'H'), KD('J', 'J'), KD('K', 'K'), KD('L', 'L'), KD('M', 'M'), KD('ù', ['ugrave', 'Ugrave', 'percent']), KD('Enter', 'Return', width=2.3, small_font=True)],
            [KD('Shift', 'Shift_L', width=1.2, small_font=True), KD('<', ['less', 'greater']), KD('W', 'W'), KD('X', 'X'), KD('C', 'C'), KD('V', 'V'), KD('B', 'B'), KD('N', 'N'), KD('?', ['question', 'comma']), KD('.', ['period', 'semicolon']), KD('/', ['slash', 'colon']), KD('§', ['section', 'exclam']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_DOT_DECIMAL
    },
    "Dvorak_US_Full": {
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('`', ['grave', 'asciitilde']), KD('1', ['1', 'exclam']), KD('2', ['2', 'at']), KD('3', ['3', 'numbersign']), KD('4', ['4', 'dollar']), KD('5', ['5', 'percent']), KD('6', ['6', 'asciicircum']), KD('7', ['7', 'ampersand']), KD('8', ['8', 'asterisk']), KD('9', ['9', 'parenleft']), KD('0', ['0', 'parenright']), KD('[', ['bracketleft', 'braceleft']), KD(']', ['bracketright', 'braceright']), KD('Backspace', 'BackSpace', width=2.0, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD("'", ['apostrophe', 'quotedbl']), KD(',', ['comma', 'less']), KD('.', ['period', 'greater']), KD('P', 'P'), KD('Y', 'Y'), KD('F', 'F'), KD('G', 'G'), KD('C', 'C'), KD('R', 'R'), KD('L', 'L'), KD('/', ['slash', 'question']), KD('=', ['equal', 'plus']), KD('\\', ['backslash', 'bar'], width=1.5)],
            [KD('Caps Lock', 'Caps_Lock', width=1.8, small_font=True), KD('A', 'A'), KD('O', 'O'), KD('E', 'E'), KD('U', 'U'), KD('I', 'I'), KD('D', 'D'), KD('H', 'H'), KD('T', 'T'), KD('N', 'N'), KD('S', 'S'), KD('-', ['minus', 'underscore']), KD('Enter', 'Return', width=2.2, small_font=True)],
            [KD('Shift', 'Shift_L', width=2.3, small_font=True), KD(';', ['semicolon', 'colon']), KD('Q', 'Q'), KD('J', 'J'), KD('K', 'K'), KD('X', 'X'), KD('B', 'B'), KD('M', 'M'), KD('W', 'W'), KD('V', 'V'), KD('Z', 'Z'), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_DOT_DECIMAL
    },
    "Colemak_US_Full": {
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('`', ['grave', 'asciitilde']), KD('1', ['1', 'exclam']), KD('2', ['2', 'at']), KD('3', ['3', 'numbersign']), KD('4', ['4', 'dollar']), KD('5', ['5', 'percent']), KD('6', ['6', 'asciicircum']), KD('7', ['7', 'ampersand']), KD('8', ['8', 'asterisk']), KD('9', ['9', 'parenleft']), KD('0', ['0', 'parenright']), KD('-', ['minus', 'underscore']), KD('=', ['equal', 'plus']), KD('Backspace', ['BackSpace','Delete'], width=2.0, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('Q', 'Q'), KD('W', 'W'), KD('F', 'F'), KD('P', 'P'), KD('G', 'G'), KD('J', 'J'), KD('L', 'L'), KD('U', 'U'), KD('Y', 'Y'), KD(';',['semicolon', 'colon']), KD('[', ['bracketleft', 'braceleft']), KD(']', ['bracketright', 'braceright']), KD('\\', ['backslash', 'bar'], width=1.5)],
            [KD('Caps Lock', 'Caps_Lock', width=1.8, small_font=True), KD('A', 'A'), KD('R', 'R'), KD('S', 'S'), KD('T', 'T'), KD('D', 'D'), KD('H', 'H'), KD('N', 'N'), KD('E', 'E'), KD('I', 'I'), KD('O', 'O'), KD("'", ['apostrophe', 'quotedbl']), KD('Enter', 'Return', width=2.2, small_font=True)],
            [KD('Shift', 'Shift_L', width=2.3, small_font=True), KD('Z', 'Z'), KD('X', 'X'), KD('C', 'C'), KD('V', 'V'), KD('B', 'B'), KD('K', 'K'), KD('M', 'M'), KD(',', ['comma', 'less']), KD('.', ['period', 'greater']), KD('/', ['slash', 'question']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_DOT_DECIMAL
    },
    "Colemak_DH_US_Full": {
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('`', ['grave', 'asciitilde']), KD('1', ['1', 'exclam']), KD('2', ['2', 'at']), KD('3', ['3', 'numbersign']), KD('4', ['4', 'dollar']), KD('5', ['5', 'percent']), KD('6', ['6', 'asciicircum']), KD('7', ['7', 'ampersand']), KD('8', ['8', 'asterisk']), KD('9', ['9', 'parenleft']), KD('0', ['0', 'parenright']), KD('-', ['minus', 'underscore']), KD('=', ['equal', 'plus']), KD('Backspace', ['BackSpace','Delete'], width=2.0, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('Q', 'Q'), KD('W', 'W'), KD('F', 'F'), KD('P', 'P'), KD('B', 'B'), KD('J', 'J'), KD('L', 'L'), KD('U', 'U'), KD('Y', 'Y'), KD(';',['semicolon', 'colon']), KD('[', ['bracketleft', 'braceleft']), KD(']', ['bracketright', 'braceright']), KD('\\', ['backslash', 'bar'], width=1.5)],
            [KD('Caps Lock', 'Caps_Lock', width=1.8, small_font=True), KD('A', 'A'), KD('R', 'R'), KD('S', 'S'), KD('T', 'T'), KD('G', 'G'), KD('M', 'M'), KD('N', 'N'), KD('E', 'E'), KD('I', 'I'), KD('O', 'O'), KD("'", ['apostrophe', 'quotedbl']), KD('Enter', 'Return', width=2.2, small_font=True)],
            [KD('Shift', 'Shift_L', width=2.3, small_font=True), KD('X', 'X'), KD('C', 'C'), KD('D', 'D'), KD('V', 'V'), KD('Z', 'Z'), KD('K', 'K'), KD('H', 'H'), KD(',', ['comma', 'less']), KD('.', ['period', 'greater']), KD('/', ['slash', 'question']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_DOT_DECIMAL
    },
    "JCUKEN_RU_Full": { # Russian Standard Layout (ЙЦУКЕН)
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('Ё', ['Cyrillic_io', 'grave', 'asciitilde']), KD('1', ['1', 'exclam']), KD('2', ['2', 'quotedbl']), KD('3', ['3', 'numerosign']), KD('4', ['4', 'semicolon']), KD('5', ['5', 'percent']), KD('6', ['6', 'colon']), KD('7', ['7', 'question']), KD('8', ['8', 'asterisk']), KD('9', ['9', 'parenleft']), KD('0', ['0', 'parenright']), KD('-', ['minus', 'underscore']), KD('=', ['equal', 'plus']), KD('Backspace', 'BackSpace', width=2.0, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('Й', 'Cyrillic_shorti'), KD('Ц', 'Cyrillic_tse'), KD('У', 'Cyrillic_u'), KD('К', 'Cyrillic_ka'), KD('Е', 'Cyrillic_ie'), KD('Н', 'Cyrillic_en'), KD('Г', 'Cyrillic_ghe'), KD('Ш', 'Cyrillic_sha'), KD('Щ', 'Cyrillic_shcha'), KD('З', 'Cyrillic_ze'), KD('Х', 'Cyrillic_ha'), KD('Ъ', 'Cyrillic_hardsign'), KD('\\', ['backslash', 'slash'], width=1.5)],
            [KD('Caps Lock', 'Caps_Lock', width=1.8, small_font=True), KD('Ф', 'Cyrillic_ef'), KD('Ы', 'Cyrillic_yeru'), KD('В', 'Cyrillic_ve'), KD('А', 'Cyrillic_a'), KD('П', 'Cyrillic_pe'), KD('Р', 'Cyrillic_er'), KD('О', 'Cyrillic_o'), KD('Л', 'Cyrillic_el'), KD('Д', 'Cyrillic_de'), KD('Ж', 'Cyrillic_zhe'), KD('Э', 'Cyrillic_e'), KD('Enter', 'Return', width=2.2, small_font=True)],
            [KD('Shift', 'Shift_L', width=2.3, small_font=True), KD('Я', 'Cyrillic_ya'), KD('Ч', 'Cyrillic_che'), KD('С', 'Cyrillic_es'), KD('М', 'Cyrillic_em'), KD('И', 'Cyrillic_i'), KD('Т', 'Cyrillic_te'), KD('Ь', 'Cyrillic_softsign'), KD('Б', 'Cyrillic_be'), KD('Ю', 'Cyrillic_yu'), KD('.', ['period', 'comma']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_DOT_DECIMAL
    },
    "Workman_US_Full": {
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('`', ['grave', 'asciitilde']), KD('1', ['1', 'exclam']), KD('2', ['2', 'at']), KD('3', ['3', 'numbersign']), KD('4', ['4', 'dollar']), KD('5', ['5', 'percent']), KD('6', ['6', 'asciicircum']), KD('7', ['7', 'ampersand']), KD('8', ['8', 'asterisk']), KD('9', ['9', 'parenleft']), KD('0', ['0', 'parenright']), KD('-', ['minus', 'underscore']), KD('=', ['equal', 'plus']), KD('Backspace', 'BackSpace', width=2.0, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('Q', 'Q'), KD('D', 'D'), KD('R', 'R'), KD('W', 'W'), KD('B', 'B'), KD('J', 'J'), KD('F', 'F'), KD('U', 'U'), KD('P', 'P'), KD(';',['semicolon', 'colon']), KD('[', ['bracketleft', 'braceleft']), KD(']', ['bracketright', 'braceright']), KD('\\', ['backslash', 'bar'], width=1.5)],
            [KD('Caps Lock', 'Caps_Lock', width=1.8, small_font=True), KD('A', 'A'), KD('S', 'S'), KD('H', 'H'), KD('T', 'T'), KD('G', 'G'), KD('Y', 'Y'), KD('N', 'N'), KD('E', 'E'), KD('O', 'O'), KD('I', 'I'), KD("'", ['apostrophe', 'quotedbl']), KD('Enter', 'Return', width=2.2, small_font=True)],
            [KD('Shift', 'Shift_L', width=2.3, small_font=True), KD('Z', 'Z'), KD('X', 'X'), KD('M', 'M'), KD('C', 'C'), KD('V', 'V'), KD('K', 'K'), KD('L', 'L'), KD(',', ['comma', 'less']), KD('.', ['period', 'greater']), KD('/', ['slash', 'question']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_DOT_DECIMAL
    },
    "Maltron_Logical_Full": { # Logical mapping of Maltron on standard rows
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('Esc', 'Escape'), KD('1', '1'), KD('2', '2'), KD('3', '3'), KD('4', '4'), KD('5', '5'), KD('6', '6'), KD('7', '7'), KD('8', '8'), KD('9', '9'), KD('0', '0'), KD('-', '-'), KD('=', '='), KD('Bksp', 'BackSpace', width=2.0)],
            [KD('Tab', 'Tab', width=1.5), KD('Q', 'Q'), KD('P', 'P'), KD('Y', 'Y'), KD('C', 'C'), KD('B', 'B'),      KD('J', 'J'), KD('L', 'L'), KD('M', 'M'), KD('F', 'F'), KD('V', 'V'), KD('Z', 'Z'), KD(']', ']'), KD('\\', '\\', width=1.5)],
            [KD('Caps', 'Caps_Lock', width=1.8), KD('A', 'A'), KD('N', 'N'), KD('I', 'I'), KD('S', 'S'), KD('F', 'F'),      KD('G', 'G'), KD('D', 'D'), KD('T', 'T'), KD('H', 'H'), KD('O', 'O'), KD('R', 'R'), KD('Enter', 'Return', width=2.2)],
            [KD('Shift', 'Shift_L', width=2.3), KD('.', '.'), KD(',', ','), KD(';', ';'), KD('K', 'K'), KD('X', 'X'),      KD('W', 'W'), KD('/', '/'), KD('[', '['), KD('"', '"'), KD('Shift', 'Shift_R', width=2.7)],
            [KD('Ctrl', 'Control_L', width=1.4), KD('Win', 'Super_L', width=1.1), KD('Alt', 'Alt_L', width=1.1), KD('E', 'E', width=2.0), KD('Space', 'space', width=2.0), KD('U', 'U', width=2.0), KD('AltGr', 'Alt_R', width=1.1), KD('Win', 'Super_R', width=1.1), KD('Menu', 'App', width=1.1), KD('Ctrl', 'Control_R', width=1.4)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_DOT_DECIMAL
    },
    "Svorak_SE_Full": { # Swedish Dvorak (Svorak A1 / Sv Dvorak)
        "f_keys_row": STD_F_KEYS_ROW,
        "main_block": [
            [KD('§', ['section', 'paragraph']), KD('1', ['1', 'exclam']), KD('2', ['2', 'quotedbl', 'at']), KD('3', ['3', 'numbersign', 'sterling']), KD('4', ['4', 'currency', 'dollar']), KD('5', ['5', 'percent']), KD('6', ['6', 'ampersand']), KD('7', ['7', 'slash', 'braceleft']), KD('8', ['8', 'parenleft', 'bracketleft']), KD('9', ['9', 'parenright', 'bracketright']), KD('0', ['0', 'equal', 'braceright']), KD('+', ['plus', 'question', 'backslash']), KD('´', ['acute', 'grave', 'dead_acute', 'dead_grave']), KD('Backspace', 'BackSpace', width=1.8, small_font=True)],
            [KD('Tab', 'Tab', width=1.5, small_font=True), KD('.', ['period', 'colon']), KD(',', ['comma', 'semicolon']), KD('K', 'K'), KD('X', 'X'), KD('B', 'B'), KD('M', 'M'), KD('W', 'W'), KD('V', 'V'), KD('Z', 'Z'), KD('Å', ['aring', 'Aring']), KD('¨', ['diaeresis', 'asciicircum', 'dead_diaeresis', 'dead_circumflex']), KD("'", ['apostrophe', 'asterisk']), KD('Return', 'Return', width=1.2, height=2.0, small_font=True)],
            [KD('Caps Lock', 'Caps_Lock', width=1.7, small_font=True), KD('A', 'A'), KD('O', 'O'), KD('E', 'E'), KD('U', 'U'), KD('I', 'I'), KD('D', 'D'), KD('H', 'H'), KD('T', 'T'), KD('N', 'N'), KD('S', 'S'), KD('Ö', ['odiaeresis', 'Odiaeresis'])],
            [KD('Shift', 'Shift_L', width=1.2, small_font=True), KD('<', ['less', 'greater', 'bar']), KD('Q', 'Q'), KD('J', 'J'), KD('G', 'G'), KD('P', 'P'), KD('R', 'R'), KD('L', 'L'), KD('C', 'C'), KD('Y', 'Y'), KD('F', 'F'), KD('Ä', ['adiaeresis', 'Adiaeresis']), KD('Shift', 'Shift_R', width=2.7, small_font=True)],
            [KD('Ctrl', 'Control_L', width=1.4, small_font=True), KD('Win', ['Super_L', 'Meta_L'], width=1.1, small_font=True), KD('Alt', 'Alt_L', width=1.1, small_font=True), KD('Space', 'space', width=6.0), KD('AltGr', ['Alt_R', 'ISO_Level3_Shift'], width=1.1, small_font=True), KD('Win', ['Super_R', 'Meta_R'], width=1.1, small_font=True), KD('Menu', ['Menu', 'App'], width=1.1, small_font=True), KD('Ctrl', 'Control_R', width=1.4, small_font=True)]
        ],
        "edit_block": STD_EDIT_BLOCK, "navigation_block": STD_NAVIGATION_BLOCK,
        "arrow_keys_block": STD_ARROW_KEYS_BLOCK, "numpad_block": STD_NUMPAD_BLOCK_COMMA_DECIMAL
    },
}
# --- End of Layout Definitions ---


# --- Base Mode Class ---
class BaseMode:
    def __init__(self, app_controller, parent_frame):
        self.app = app_controller
        self.root = app_controller.root
        self.frame = tk.Frame(parent_frame, bg=STYLE_CONFIG["content_frame_bg"])

    def activate(self):
        if self.frame.winfo_exists():
            self.frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        else:
            self.frame = tk.Frame(self.app.content_frame, bg=STYLE_CONFIG["content_frame_bg"])
            self._build_ui()
            self.frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    def deactivate(self):
        if self.frame.winfo_exists():
            self.frame.pack_forget()

    def destroy_ui(self):
        if self.frame.winfo_exists():
            for widget in self.frame.winfo_children():
                if widget.winfo_exists():
                    widget.destroy()

    def _build_ui(self):
        pass

    def on_key_press(self, event): pass
    def on_key_release(self, event): pass

    def update_app_info_label(self, text):
        if self.app.info_label and self.app.info_label.winfo_exists():
            self.app.info_label.config(text=text)

# --- Visual Keyboard Display Mode ---
class VisualKeyboardDisplayMode(BaseMode):
    def __init__(self, app_controller, parent_frame):
        super().__init__(app_controller, parent_frame)
        self.avg_char_width = self.app.avg_char_width
        self.key_widgets_map = {}
        self.widget_to_key_def = {}
        self.default_bg_colors = {}
        self.modifier_keys_state = {
            'Shift_L': False, 'Shift_R': False, 'Control_L': False, 'Control_R': False,
            'Alt_L': False, 'Alt_R': False, 'ISO_Level3_Shift': False, 'Caps_Lock': False,
            'Num_Lock': True, 'Super_L': False, 'Super_R': False, 'Meta_L': False, 'Meta_R': False
        }
        self.active_toggle_widgets = {}
        self.currently_pressed_physical_keys = set()
        self._build_ui()

    def _build_ui(self):
        super()._build_ui()
        mode_control_frame = tk.Frame(self.frame, bg=STYLE_CONFIG["content_frame_bg"])
        mode_control_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(mode_control_frame, text="Keyboard Layout:", bg=STYLE_CONFIG["content_frame_bg"], fg=STYLE_CONFIG["info_fg"], font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"])).pack(side=tk.LEFT, padx=(0,5))
        self.layout_var = tk.StringVar(master=self.root, value=list(LAYOUTS.keys())[0])
        layout_menu = ttk.Combobox(mode_control_frame, textvariable=self.layout_var, values=list(LAYOUTS.keys()), state="readonly", width=20, font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"]))
        layout_menu.pack(side=tk.LEFT, padx=5)
        layout_menu.bind("<<ComboboxSelected>>", self.on_layout_config_change)
        self.keyboard_draw_area = tk.Frame(self.frame, bg=STYLE_CONFIG["content_frame_bg"])
        self.keyboard_draw_area.pack(expand=True, fill=tk.BOTH)
        self.draw_visual_keyboard(self.layout_var.get())

    def on_layout_config_change(self, event=None):
        self.draw_visual_keyboard(self.layout_var.get())
        if self.root.winfo_exists(): self.root.focus_set()

    def _create_key_button(self, parent_frame, key_def):
        if key_def == SPACER:
            spacer_width_chars = STYLE_CONFIG["base_key_width"] * 0.25
            spacer_width_px = int(spacer_width_chars * self.avg_char_width / 2.5)
            spacer = tk.Frame(parent_frame, width=max(5, spacer_width_px), height=1, bg=STYLE_CONFIG["content_frame_bg"])
            spacer.pack(side=tk.LEFT)
            return None
        label = key_def['label']
        width = int(STYLE_CONFIG["base_key_width"] * key_def['width_factor'])
        height = int(STYLE_CONFIG["base_key_height"] * key_def['height_factor'])
        font_size = STYLE_CONFIG["font_size_small"] if key_def.get('small_font') else STYLE_CONFIG["font_size_normal"]
        btn = tk.Button(parent_frame, text=label, width=width, height=height, bg=STYLE_CONFIG["key_bg"], fg=STYLE_CONFIG["key_fg"], font=(STYLE_CONFIG["font_family"], font_size), relief=STYLE_CONFIG["key_relief"], borderwidth=STYLE_CONFIG["key_borderwidth"], highlightthickness=STYLE_CONFIG["highlight_thickness"], activebackground=STYLE_CONFIG["key_pressed_bg"], activeforeground=STYLE_CONFIG["key_fg"])
        ipady_val = 3 if key_def['height_factor'] > 1.5 else 1
        padx_val, pady_val = (1,1)
        if key_def['width_factor'] < 0.8 or key_def['height_factor'] < 0.8 : padx_val, pady_val = (0,0); ipady_val = 0
        btn.pack(side=tk.LEFT, padx=padx_val, pady=pady_val, ipady=ipady_val)
        self.default_bg_colors[btn] = STYLE_CONFIG["key_bg"]
        self.widget_to_key_def[btn] = key_def
        all_identifiers = set(key_def['keysyms'])
        if key_def.get('char_override'): all_identifiers.add(key_def['char_override'])
        for identifier in all_identifiers:
            processed_id = str(identifier).lower()
            if processed_id not in self.key_widgets_map: self.key_widgets_map[processed_id] = []
            self.key_widgets_map[processed_id].append(btn)
        if 'Caps_Lock' in key_def['keysyms']: self.active_toggle_widgets['Caps_Lock'] = btn
        if 'Num_Lock' in key_def['keysyms']: self.active_toggle_widgets['Num_Lock'] = btn
        return btn

    def _draw_key_group(self, parent_frame, group_keys_list, group_id_prefix):
        for r_idx, row_keys in enumerate(group_keys_list):
            row_frame = tk.Frame(parent_frame, bg=STYLE_CONFIG["content_frame_bg"])
            if group_id_prefix == "main" and r_idx > 0 :
                indent_factor = 0
                if r_idx == 1: indent_factor = 0.6
                elif r_idx == 2: indent_factor = 0.9
                elif r_idx == 3: indent_factor = 1.25
                if indent_factor > 0:
                    indent_width_px = int(STYLE_CONFIG["base_key_width"] * indent_factor * self.avg_char_width / 7)
                    tk.Frame(row_frame, width=indent_width_px, bg=STYLE_CONFIG["content_frame_bg"]).pack(side=tk.LEFT)
            row_frame.pack(anchor=tk.W)
            for key_def in row_keys:
                self._create_key_button(row_frame, key_def)

    def draw_visual_keyboard(self, layout_name):
        if not self.keyboard_draw_area.winfo_exists(): return
        for widget in self.keyboard_draw_area.winfo_children():
            if widget.winfo_exists(): widget.destroy()
        self.key_widgets_map.clear(); self.widget_to_key_def.clear();
        self.default_bg_colors.clear(); self.active_toggle_widgets.clear()
        layout_config = LAYOUTS.get(layout_name)
        if not layout_config: return
        fkey_edit_outer_frame = tk.Frame(self.keyboard_draw_area, bg=STYLE_CONFIG["content_frame_bg"])
        fkey_edit_outer_frame.pack(fill=tk.X, pady=(0,5), anchor=tk.N)
        fkey_block_frame = tk.Frame(fkey_edit_outer_frame, bg=STYLE_CONFIG["content_frame_bg"])
        self._draw_key_group(fkey_block_frame, layout_config["f_keys_row"], "fkeys")
        fkey_block_frame.pack(side=tk.LEFT, anchor=tk.NW)
        tk.Frame(fkey_edit_outer_frame, width=30, bg=STYLE_CONFIG["content_frame_bg"]).pack(side=tk.LEFT)
        if "edit_block" in layout_config:
            edit_block_frame = tk.Frame(fkey_edit_outer_frame, bg=STYLE_CONFIG["content_frame_bg"])
            self._draw_key_group(edit_block_frame, layout_config["edit_block"], "edit")
            edit_block_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=(0,15))
        center_row_frame = tk.Frame(self.keyboard_draw_area, bg=STYLE_CONFIG["content_frame_bg"])
        center_row_frame.pack(fill=tk.X, pady=5, anchor=tk.N)
        main_block_frame = tk.Frame(center_row_frame, bg=STYLE_CONFIG["content_frame_bg"])
        self._draw_key_group(main_block_frame, layout_config["main_block"], "main")
        main_block_frame.pack(side=tk.LEFT, anchor=tk.NW)
        nav_arrow_cluster_frame = tk.Frame(center_row_frame, bg=STYLE_CONFIG["content_frame_bg"])
        nav_arrow_cluster_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=(25, 0))
        if "navigation_block" in layout_config:
            nav_block_frame = tk.Frame(nav_arrow_cluster_frame, bg=STYLE_CONFIG["content_frame_bg"])
            self._draw_key_group(nav_block_frame, layout_config["navigation_block"], "nav")
            nav_block_frame.pack(anchor=tk.NW, pady=(0,10))
        if "arrow_keys_block" in layout_config:
            arrow_block_frame = tk.Frame(nav_arrow_cluster_frame, bg=STYLE_CONFIG["content_frame_bg"])
            self._draw_key_group(arrow_block_frame, layout_config["arrow_keys_block"], "arrow")
            arrow_block_frame.pack(anchor=tk.CENTER)
        if "numpad_block" in layout_config:
            numpad_frame = tk.Frame(center_row_frame, bg=STYLE_CONFIG["content_frame_bg"])
            self._draw_key_group(numpad_frame, layout_config["numpad_block"], "num")
            numpad_frame.pack(side=tk.LEFT, anchor=tk.NW, padx=(20,0))
        self.update_all_modifier_visuals()
        if self.root.winfo_exists(): self.root.update_idletasks()

    def update_all_modifier_visuals(self):
        for mod_key_name, widget in self.active_toggle_widgets.items():
            is_active = self.modifier_keys_state.get(mod_key_name, False)
            bg = STYLE_CONFIG["key_active_modifier_bg"] if is_active else self.default_bg_colors.get(widget, STYLE_CONFIG["key_bg"])
            if widget.winfo_exists(): widget.config(bg=bg)
        for mod_ks_name, is_held in self.modifier_keys_state.items():
            if mod_ks_name in self.active_toggle_widgets: continue
            widgets_to_update = self.key_widgets_map.get(mod_ks_name.lower(), [])
            for widget in widgets_to_update:
                if not widget.winfo_exists(): continue
                if is_held:
                    widget.config(bg=STYLE_CONFIG["key_active_modifier_bg"], relief=tk.SUNKEN)
                elif not any(pk == mod_ks_name for pk in self.currently_pressed_physical_keys):
                    key_def = self.widget_to_key_def.get(widget)
                    is_active_toggle = key_def and any(mks in self.active_toggle_widgets and self.modifier_keys_state.get(mks) for mks in key_def['keysyms'])
                    if not is_active_toggle:
                        widget.config(bg=self.default_bg_colors.get(widget, STYLE_CONFIG["key_bg"]), relief=STYLE_CONFIG["key_relief"])

    def _find_widgets_for_event(self, keysym, char):
        widgets = set()
        for w_check, kd_check in self.widget_to_key_def.items():
            if kd_check.get('char_override') == char and char and w_check.winfo_exists():
                widgets.add(w_check)
                return list(widgets)
        keys_to_check = {keysym, keysym.lower(), keysym.upper()}
        if char: keys_to_check.add(char)
        for k_check in keys_to_check:
            norm_k = str(k_check).lower()
            if norm_k in self.key_widgets_map:
                for w_item in self.key_widgets_map[norm_k]:
                    if w_item.winfo_exists(): widgets.add(w_item)
        return list(widgets)

    def on_key_press(self, event):
        super().update_app_info_label(f"Press: {event.keysym} (char: '{event.char}')")
        keysym = event.keysym; char = event.char
        self.currently_pressed_physical_keys.add(keysym)
        if keysym in self.active_toggle_widgets: self.modifier_keys_state[keysym] = not self.modifier_keys_state[keysym]
        elif keysym in self.modifier_keys_state: self.modifier_keys_state[keysym] = True
        self.update_all_modifier_visuals()
        target_widgets = self._find_widgets_for_event(keysym, char)
        for widget in target_widgets:
            if not widget.winfo_exists(): continue
            key_def = self.widget_to_key_def.get(widget)
            is_modifier_widget = key_def and any(mks in self.modifier_keys_state for mks in key_def['keysyms'])
            if not is_modifier_widget or keysym not in self.active_toggle_widgets: widget.config(bg=STYLE_CONFIG["key_pressed_bg"], relief=tk.SUNKEN)

    def on_key_release(self, event):
        super().update_app_info_label(f"Release: {event.keysym}")
        keysym = event.keysym; char = event.char
        if keysym in self.currently_pressed_physical_keys: self.currently_pressed_physical_keys.remove(keysym)
        if keysym in self.modifier_keys_state and keysym not in self.active_toggle_widgets: self.modifier_keys_state[keysym] = False
        self.update_all_modifier_visuals()
        target_widgets = self._find_widgets_for_event(keysym, char)
        for widget in target_widgets:
            if not widget.winfo_exists(): continue
            key_def = self.widget_to_key_def.get(widget)
            is_active_toggle_mod = key_def and any(mks in self.active_toggle_widgets and self.modifier_keys_state.get(mks) for mks in key_def['keysyms'])
            is_active_held_mod = key_def and any(mks in self.modifier_keys_state and self.modifier_keys_state.get(mks) and mks not in self.active_toggle_widgets for mks in key_def['keysyms'])
            if is_active_toggle_mod or is_active_held_mod:
                widget.config(bg=STYLE_CONFIG["key_active_modifier_bg"], relief=STYLE_CONFIG["key_relief"])
            else:
                widget.config(bg=self.default_bg_colors.get(widget, STYLE_CONFIG["key_bg"]), relief=STYLE_CONFIG["key_relief"])

# --- Simple Event Logger Mode ---
class EventLoggerMode(BaseMode):
    def __init__(self, app_controller, parent_frame):
        super().__init__(app_controller, parent_frame)
        self._build_ui()

    def _build_ui(self):
        super()._build_ui()
        tk.Label(self.frame, text="Raw Key Event Log:", bg=STYLE_CONFIG["content_frame_bg"],
                 fg=STYLE_CONFIG["info_fg"], font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"]+2, "bold")
                 ).pack(pady=(5,2), anchor=tk.W)
        self.log_text = ScrolledText(self.frame, height=15, width=80, wrap=tk.WORD,
                                     bg=STYLE_CONFIG["text_widget_bg"], fg=STYLE_CONFIG["text_widget_fg"],
                                     font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"]),
                                     relief=tk.FLAT, borderwidth=1,
                                     insertbackground=STYLE_CONFIG["key_fg"])
        self.log_text.pack(expand=True, fill=tk.BOTH, pady=5)
        self.log_text.config(state=tk.DISABLED)
        clear_button = tk.Button(self.frame, text="Clear Log", command=self.clear_log,
                                 bg=STYLE_CONFIG["key_bg"], fg=STYLE_CONFIG["key_fg"],
                                 activebackground=STYLE_CONFIG["key_pressed_bg"],
                                 font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"]),
                                 relief=STYLE_CONFIG["key_relief"])
        clear_button.pack(pady=5)

    def log_event(self, event_type, event):
        if not self.log_text.winfo_exists(): return
        self.log_text.config(state=tk.NORMAL)
        log_entry = f"{event_type:<10} Keysym: '{event.keysym}', Char: '{event.char}', KeyCode: {event.keycode}, State: {hex(event.state)}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        super().update_app_info_label(f"{event_type}: {event.keysym} (char: '{event.char}')")

    def on_key_press(self, event): self.log_event("Press", event)
    def on_key_release(self, event): self.log_event("Release", event)
    def clear_log(self):
        if not self.log_text.winfo_exists(): return
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        super().update_app_info_label("Log cleared.")

# --- Main Application Controller ---
class KeyboardTesterApp:
    def __init__(self, root):
        self.root = root
        root.title("Keyboard Tester Pro")
        root.configure(bg=STYLE_CONFIG["window_bg"])
        root.minsize(750, 600)

        self.font_normal_obj = tkinter.font.Font(family=STYLE_CONFIG["font_family"], size=STYLE_CONFIG["font_size_normal"])
        self.avg_char_width = self.font_normal_obj.measure("0")

        self.active_mode_instance = None
        self.modes = {
            "Visual Keyboard": VisualKeyboardDisplayMode,
            "Event Logger": EventLoggerMode
        }

        top_control_frame = tk.Frame(root, bg=STYLE_CONFIG["window_bg"], pady=10)
        top_control_frame.pack(fill=tk.X)
        tk.Label(top_control_frame, text="Tester Mode:", bg=STYLE_CONFIG["window_bg"], fg=STYLE_CONFIG["info_fg"],
                 font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"])).pack(side=tk.LEFT, padx=(10,0))
        self.mode_var = tk.StringVar(master=self.root, value=list(self.modes.keys())[0])
        s = ttk.Style()
        s.theme_use('clam')
        combobox_bg = STYLE_CONFIG["key_bg"]; combobox_fg = STYLE_CONFIG["key_fg"]
        s.configure('TCombobox', fieldbackground=combobox_bg, background=combobox_bg, foreground=combobox_fg, selectbackground=combobox_bg, selectforeground=combobox_fg, arrowcolor=combobox_fg, borderwidth=0, padding=3, lightcolor=combobox_bg, darkcolor=combobox_bg)
        s.map('TCombobox', fieldbackground=[('readonly', combobox_bg)], selectbackground=[('readonly', combobox_bg)], selectforeground=[('readonly', combobox_fg)], foreground=[('readonly', combobox_fg)])
        mode_menu = ttk.Combobox(top_control_frame, textvariable=self.mode_var, values=list(self.modes.keys()), state="readonly", width=18, font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"]))
        mode_menu.pack(side=tk.LEFT, padx=5)
        mode_menu.bind("<<ComboboxSelected>>", self.on_app_mode_change)
        self.info_label = tk.Label(top_control_frame, text="Select a mode to begin. Esc to close.", bg=STYLE_CONFIG["window_bg"], fg=STYLE_CONFIG["info_fg"], font=(STYLE_CONFIG["font_family"], STYLE_CONFIG["font_size_normal"]))
        self.info_label.pack(side=tk.LEFT, padx=20, expand=True, fill=tk.X)

        self.content_frame = tk.Frame(root, bg=STYLE_CONFIG["content_frame_bg"])
        self.content_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        self.switch_mode(self.mode_var.get())

        root.bind("<KeyPress>", self._handle_key_press)
        root.bind("<KeyRelease>", self._handle_key_release)
        root.bind("<Escape>", lambda e: self.root.destroy() if self.root.winfo_exists() else None)
        if self.root.winfo_exists(): root.focus_set()

    def on_app_mode_change(self, event=None):
        selected_mode_name = self.mode_var.get()
        self.switch_mode(selected_mode_name)

    def switch_mode(self, mode_name):
        if self.active_mode_instance:
            self.active_mode_instance.deactivate()
            self.active_mode_instance.destroy_ui()

        mode_class = self.modes.get(mode_name)
        if mode_class:
            self.active_mode_instance = mode_class(self, self.content_frame)
            self.active_mode_instance.activate()
            if self.info_label.winfo_exists():
                self.info_label.config(text=f"{mode_name} active. Esc to close.")
        else:
            self.active_mode_instance = None
            if self.info_label.winfo_exists():
                self.info_label.config(text="Error: Selected mode not found.")
        if self.root.winfo_exists(): self.root.focus_set()

    def _handle_key_press(self, event):
        if self.active_mode_instance and hasattr(self.active_mode_instance, 'on_key_press'):
            self.active_mode_instance.on_key_press(event)
    def _handle_key_release(self, event):
        if self.active_mode_instance and hasattr(self.active_mode_instance, 'on_key_release'):
            self.active_mode_instance.on_key_release(event)

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyboardTesterApp(root)
    root.mainloop()