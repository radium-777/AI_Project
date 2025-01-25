import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtCore import Qt
from window import ChatOverlay


def main():
    app = QApplication(sys.argv)

    # Create the chat overlay window
    chat_overlay = ChatOverlay()
    chat_overlay.show()

    # Simulate adding messages from an external API
    chat_overlay.add_message("API: Welcome to the chat!")
    chat_overlay.add_message("API: Feel free to type a message.")

    shortcut = QShortcut(QKeySequence(Qt.ALT + Qt.Key_G), chat_overlay)
    shortcut.activated.connect(chat_overlay.toggle_visibility)
    
    sys.exit(app.exec_())

def capture_screenshot():
    # Capture the entire screen
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    print("Screenshot saved as 'screenshot.png'")

if __name__ == "__main__":
    main()
