import sys
import os
from PySide6.QtWidgets import QApplication
import pyautogui
import time
import keyboard
from window import ChatOverlay
from ocr import do_ocr


def main():
    app = QApplication(sys.argv)

    # Create the chat overlay window
    chat_overlay = ChatOverlay(callback_user_message_trigger)
    chat_overlay.show()

    # Simulate adding messages from an external API
    chat_overlay.add_message("API: Welcome to the chat!")
    chat_overlay.add_message("API: Feel free to type a message.")

    keyboard.add_hotkey("alt+g", chat_overlay.toggle_visibility)
    keyboard.add_hotkey("alt+h", capture_screenshot)

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

    file = open(path, "rb")
    print(do_ocr(file))

    return path
    
def callback_user_message_trigger(chat_overlay):
    print("User sent message: " + chat_overlay.messages[-1])

if __name__ == "__main__":
    main()
