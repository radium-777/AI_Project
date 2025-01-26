import sys
import os
from PySide6.QtWidgets import QApplication
import pyautogui
import time
import keyboard
from window import ChatOverlay


def main():
    app = QApplication(sys.argv)

    # Create the chat overlay window
    chat_overlay = ChatOverlay()
    chat_overlay.show()

    # Simulate adding messages from an external API
    chat_overlay.add_message("API: Welcome to the chat!")
    chat_overlay.add_message("API: Feel free to type a message.")

    keyboard.add_hotkey("alt+g", chat_overlay.toggle_visibility)

    chat_overlay.wait_for_message()

    print("Done")

    sys.exit(app.exec_())

def capture_screenshot():
    # Capture the entire screen
    screenshot = pyautogui.screenshot()

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.png"

    cwd = os.getcwd()
    
    if not os.path.isdir(cwd+"/.local/"):
        os.mkdir(cwd+"/.local/")

    path = cwd+"/.local/"+filename
    screenshot.save(path)
    return path
    

if __name__ == "__main__":
    main()
