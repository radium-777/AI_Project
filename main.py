import sys
from PySide6.QtWidgets import QApplication
from window import ChatOverlay


def main():
    app = QApplication(sys.argv)

    # Create the chat overlay window
    chat_overlay = ChatOverlay()
    chat_overlay.show()

    # Simulate adding messages from an external API
    chat_overlay.add_message("API: Welcome to the chat!")
    chat_overlay.add_message("API: Feel free to type a message.")

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
