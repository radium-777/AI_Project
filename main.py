import sys
import os
from PySide6.QtWidgets import QApplication
import pyautogui
import time
import keyboard
from window import ChatOverlay
from ocr import do_ocr
from chatapi import ChatAPI

app = QApplication(sys.argv)
chat_overlay = ChatOverlay()
chat_api = ChatAPI()

ocr_data = []

def main():
    # Create the chat overlay window
    chat_overlay.show()
    chat_overlay.callback_user_message_trigger = callback_user_message_trigger

    # Simulate adding messages from an external API
    chat_overlay.add_message("API: How can I help you?")

    keyboard.add_hotkey("alt+g", chat_overlay.toggle_visibility)
    keyboard.add_hotkey("alt+h", capture_screenshot)

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
    ocrstring = do_ocr(file)
    ocr_data.append(ocrstring)

    chat_overlay.messages.append("[IMAGE]")

    chat_overlay.messages.append("API: " + chat_api.messageQuery(str(chat_overlay.messages), str(ocr_data)))

    chat_overlay.screenshot_signal.emit()

    return path
    
def callback_user_message_trigger(chat_overlay):
    chat_overlay.add_message("API: " + chat_api.messageQuery(str(chat_overlay.messages) + str(ocr_data), ""))

if __name__ == "__main__":
    main()
