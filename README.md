# Python Visual Keyboard Tester Pro

A comprehensive, multi-mode keyboard testing utility built with Python and Tkinter. It allows users to visually test their keyboard layouts, identify key presses and releases, and log raw keyboard events.

## Features

*   **Multiple Tester Modes:**
    *   **Visual Keyboard:** Displays a graphical representation of various keyboard layouts. Highlights keys as they are physically pressed.
    *   **Event Logger:** Logs raw key press and release event details (keysym, char, keycode, state) in a text area.
*   **Extensive Layout Support:** Includes definitions for a wide range of common and alternative keyboard layouts:
    *   QWERTY (US)
    *   Spanish (ES)
    *   German (DE - QWERTZ)
    *   French (FR - AZERTY)
    *   Dvorak (US)
    *   Colemak (US)
    *   Colemak-DH (US)
    *   JCUKEN (RU - Russian)
    *   Workman (US)
    *   Maltron (Logical Representation)
    *   Svorak (SE - Swedish Dvorak)
*   **Visual Feedback:**
    *   Keys highlight on the visual keyboard upon press.
    *   Modifier keys (Shift, Ctrl, Alt, Win/Super) show a distinct "held" state.
    *   Toggle keys (Caps Lock, Num Lock) show an "active" state.
*   **Dark Theme:** Monkeytype-inspired dark theme for a modern look and feel.
*   **Cross-Platform (Tkinter-based):** Should run on Windows, macOS, and Linux where Python and Tkinter are available.
*   **Informative Display:** Shows `keysym`, `char`, `keycode`, and modifier state for pressed keys.

## Prerequisites

*   **Python 3.x:** The script is written for Python 3.
*   **Tkinter:** Usually included with standard Python installations. If not (e.g., on some Linux distros), you may need to install it separately.
    *   On Debian/Ubuntu: `sudo apt-get install python3-tk`
    *   On Fedora: `sudo dnf install python3-tkinter`

## How to Run

1.  **Save the Code:** Save the Python script as a `.py` file (e.g., `keyboard_tester_pro.py`).
2.  **Open a Terminal or Command Prompt:** Navigate to the directory where you saved the file.
3.  **Run the Script:**
    ```bash
    python keyboard_tester_pro.py
    ```

## Usage

1.  **Select Tester Mode:**
    *   Use the "Tester Mode" dropdown at the top to choose between "Visual Keyboard" or "Event Logger".

2.  **Visual Keyboard Mode:**
    *   **Select Layout:** Use the "Keyboard Layout" dropdown to pick the layout you want to test or visualize. The display will update accordingly.
    *   **Test Keys:** Press keys on your physical keyboard. The corresponding keys on the visual layout will highlight:
        *   **Normal Press:** Light blue background, sunken relief.
        *   **Modifier Held (Shift, Ctrl, Alt, Win):** Green background, sunken relief.
        *   **Toggle Active (Caps Lock, Num Lock):** Green background, normal relief.
    *   **Information:** The info bar at the top will show details of the last key press/release.

3.  **Event Logger Mode:**
    *   **Test Keys:** Press keys on your physical keyboard.
    *   **Log:** Raw event details (type, keysym, char, keycode, state) will be appended to the text area.
    *   **Clear Log:** Click the "Clear Log" button to empty the text area.
    *   **Information:** The info bar at the top will show details of the last key press/release.

4.  **Exiting:** Press the `Esc` key to close the application.

## Troubleshooting

*   **`RuntimeError: Too early to ...` / `_tkinter.TclError: bad window path name`:**
    These errors usually indicate issues with Tkinter's initialization timing or widget lifecycles. The current version aims to address these, but if they occur, ensure your Python and Tkinter installation is standard.
*   **Keys Not Highlighting Correctly (Visual Mode):**
    The `keysym` (symbolic name for a key) reported by your operating system and Tkinter might differ slightly from the ones defined in the `LAYOUTS` dictionary for a specific key or layout.
    1.  Switch to "Event Logger" mode.
    2.  Press the problematic key. Note the exact `Keysym` value shown in the log.
    3.  Open the Python script and find the relevant layout in the `LAYOUTS` dictionary.
    4.  Update the `keysyms` list for the corresponding `KD(...)` definition with the `Keysym` you observed.
*   **Font Issues:** The application attempts to use "Segoe UI" (common on Windows) and falls back to "Arial". If neither is available or you prefer a different font, you can change the `font_family` in the `STYLE_CONFIG` dictionary at the beginning of the script.
*   **Dark Theme on macOS/Linux:** The dark theming of `ttk.Combobox` can sometimes be inconsistent across different operating systems and desktop environments due to how `ttk` interacts with native themes. The `clam` theme is used for `ttk` widgets to provide a more consistent appearance.

## Extending with More Layouts

To add a new keyboard layout:

1.  Open the Python script (`keyboard_tester_pro.py`).
2.  Locate the `LAYOUTS` dictionary.
3.  Add a new entry for your layout, following the structure of existing layouts (e.g., `QWERTY_Full_US` or `German_DE_Full`).
    *   Define the `main_block` with rows of keys using the `KD()` helper function.
    *   Specify the correct `label` (text on the keycap) and a list of `keysyms` (Tkinter event.keysym values) for each key.
    *   You can reuse `STD_F_KEYS_ROW`, `STD_EDIT_BLOCK`, etc., for common peripheral key blocks.
    *   Example for a new key: `KD('€', ['EuroSign', ' cinquième'], width=1.0)`
4.  Save the script. The new layout will appear in the "Keyboard Layout" dropdown.

## Code Structure Overview

*   **`STYLE_CONFIG`:** Dictionary for theming and styling constants.
*   **`KD()` function:** Helper to create key definition dictionaries for layouts.
*   **`SPACER` & `STD_...` variables:** Definitions for common key blocks (F-keys, numpad, etc.).
*   **`LAYOUTS` dictionary:** The core data structure defining all supported keyboard layouts.
*   **`BaseMode` class:** Parent class for different application modes, handling common activation/deactivation and UI lifecycle.
*   **`VisualKeyboardDisplayMode(BaseMode)`:** Implements the graphical keyboard display and testing logic.
*   **`EventLoggerMode(BaseMode)`:** Implements the raw key event logging functionality.
*   **`KeyboardTesterApp` class:** The main application controller, managing modes, top-level UI, and event delegation.

## Contributing

Contributions, bug reports, and feature requests are welcome! Please feel free to open an issue or submit a pull request if you have improvements. When adding new layouts, ensure `keysym` accuracy for common operating systems.

## License

This project is open-source. You can consider adding a license file (e.g., MIT, GPL) if you plan to distribute it more widely. For now, assume it's free to use and modify.

    # keyboardtesterpy
