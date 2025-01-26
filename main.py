import sys
import os
from PySide6.QtWidgets import QApplication
import pyautogui
import time
import keyboard
from window import ChatOverlay
from ocr import do_ocr
from chatapi import ChatAPI
from PySide6.QtCore import Signal
import pickle

app = QApplication(sys.argv)
chat_overlay = ChatOverlay()
chat_api = ChatAPI()

ocr_data = []

messages_update_signal = Signal()
ocr_data_update_signal = Signal()

cwd = os.getcwd()

if not os.path.isdir(cwd+"/.local/"):
    os.mkdir(cwd+"/.local/")


def main():
    if os.path.isfile(cwd+"/.local/message_history.pkl"):
        restore_messages_from_file()
        chat_overlay.screenshot_signal.emit()
    if os.path.isfile(cwd+"/.local/ocr_data_history.pkl"):
        restore_ocr_data_from_file()

    # Create the chat overlay window
    chat_overlay.show()
    chat_overlay.callback_user_message_trigger = callback_user_message_trigger

    # Simulate adding messages from an external API
    chat_overlay.add_message("API: How can I help you?")

    keyboard.add_hotkey("alt+g", chat_overlay.toggle_visibility)
    keyboard.add_hotkey("alt+h", capture_screenshot)

    messages_update_signal.connect(update_messages_file)
    ocr_data_update_signal.connect(update_ocr_data_file)

    sys.exit(app.exec_())

def capture_screenshot():
    # Capture the entire screen
    screenshot = pyautogui.screenshot()

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}.png"

    path = cwd+"/.local/"+filename
    screenshot.save(path)

    file = open(path, "rb")
    ocrstring = do_ocr(file)
    ocr_data.append(ocrstring)

    chat_overlay.messages.append("[IMAGE]")

    chat_overlay.messages.append("ADAM: " + chat_api.messageQuery(str(chat_overlay.messages), str(ocr_data)))

    chat_overlay.screenshot_signal.emit()

    return path
    
def callback_user_message_trigger(chat_overlay):
    chat_overlay.add_message("ADAM: " + chat_api.messageQuery(str(chat_overlay.messages), str(ocr_data)))

def update_messages_file():
    file_path = cwd+"/.local/message_history.pkl"
    with open(file_path, "wb") as file:
        pickle.dump(chat_overlay.messages, file)

def restore_messages_from_file():
    file_path = cwd+"/.local/message_history.pkl"
    with open(file_path, "rb") as file:
        chat_overlay.messages = pickle.load(file)

def update_ocr_data_file():
    file_path = cwd+"/.local/ocr_data_history.pkl"
    with open(file_path, "wb") as file:
        pickle.dump(ocr_data, file)

def restore_ocr_data_from_file():
    file_path = cwd+"/.local/ocr_data_history.pkl"
    with open(file_path, "rb") as file:
        ocr_data = pickle.load(file)

if __name__ == "__main__":
    main()
