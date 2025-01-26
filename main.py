import sys
import os
from PySide6.QtWidgets import QApplication
import pyautogui
import time
import keyboard
from window import ChatOverlay
from ocr import do_ocr
from chatapi import ChatAPI
from PySide6.QtCore import Signal, QObject, QEvent
import pickle

app = QApplication(sys.argv)
chat_overlay = ChatOverlay()
chat_api = ChatAPI()

ocr_data = {}

cwd = os.getcwd()

if not os.path.isdir(cwd+"/.local/"):
    os.mkdir(cwd+"/.local/")
if not os.path.isdir(cwd+"/files/"):
    os.mkdir(cwd+"/files/")

def main():
    if os.path.isfile(cwd+"/.local/message_history.pkl"):
        restore_messages_from_file()
        chat_overlay.screenshot_signal.emit()
    if os.path.isfile(cwd+"/.local/ocr_data_history.pkl"):
        restore_ocr_data_from_file()

    # Create the chat overlay window
    chat_overlay.show()
    chat_overlay.callback_user_message_trigger = callback_user_message_trigger
    chat_overlay.callback_update_messages_file = update_messages_file
    chat_overlay.callback_update_ocr_data_file = update_ocr_data_file
    chat_overlay.messages_update_signal.connect(chat_overlay.callback_update_messages_file)
    chat_overlay.ocr_data_update_signal.connect(chat_overlay.callback_update_ocr_data_file)

    # Simulate adding messages from an external API
    if len(chat_overlay.messages) == 0:
        chat_overlay.add_message("ADAM: How can I help you?")

    keyboard.add_hotkey("alt+g", chat_overlay.toggle_visibility)
    keyboard.add_hotkey("alt+h", capture_screenshot)

    sys.exit(app.exec_())

def capture_screenshot():
    chat_overlay.hide()

    # Capture the entire screen
    screenshot = pyautogui.screenshot()

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"SCREENSHOT_{timestamp}.png"

    path = cwd+"/.local/"+filename
    screenshot.save(path)
    
    chat_overlay.messages.append("[IMAGE]")

    chat_overlay.screenshot_signal.emit()

    file = open(path, "rb")
    ocrstring = do_ocr(file)

    ocr_data[filename] = ocrstring

    response = chat_api.messageQuery(str(chat_overlay.messages), str(ocr_data))

    cut_response = parse(response)

    if len(cut_response) > 0:
        chat_overlay.messages.append("ADAM: " + cut_response)
        chat_overlay.screenshot_signal.emit()
        chat_overlay.messages_update_signal.emit()
        chat_overlay.ocr_data_update_signal.emit()

        new_response = find_files(cwd+"/files/")
        chat_overlay.messages.append("ADAM: " + chat_api.messageQuery(str(chat_overlay.messages), str(ocr_data)))

    else:
        chat_overlay.messages.append("ADAM: " + response)
        chat_overlay.screenshot_signal.emit()
        chat_overlay.messages_update_signal.emit()
        chat_overlay.ocr_data_update_signal.emit()

    return path
    
def callback_user_message_trigger(chat_overlay):
    response = chat_api.messageQuery(str(chat_overlay.messages), str(ocr_data))
    
    cut_response = parse(response)

    if len(cut_response) > 0:
        chat_overlay.messages.append("ADAM: " + cut_response)
        chat_overlay.screenshot_signal.emit()
        chat_overlay.messages_update_signal.emit()
        chat_overlay.ocr_data_update_signal.emit()

        new_response = find_files(cwd+"/files/")
        chat_overlay.messages.append("ADAM: " + chat_api.messageQuery(str(chat_overlay.messages), str(ocr_data)))

    else:
        chat_overlay.messages.append("ADAM: " + response)
        chat_overlay.screenshot_signal.emit()
        chat_overlay.messages_update_signal.emit()
        chat_overlay.ocr_data_update_signal.emit()

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

def parse(message):
    if message.endswith('/read_files'):
        return message[:-len('/read_files')]
    else:
        return ""

def find_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Check if it is a file
        if os.path.isfile(file_path):
            # Check if the file is an image based on its extension
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
                file = open(file_path, 'rb')
                ocr_data[file_path] = do_ocr(file)
            else:
                # Process as a non-image file
                file = open(file_path, 'r', encoding='utf-8')
                ocr_data[file_path] = file.read()
                
        elif os.path.isdir(file_path):
            find_files(file_path)

if __name__ == "__main__":
    main()
