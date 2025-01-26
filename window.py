import sys
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTextEdit, QLineEdit, QWidget
from PySide6.QtCore import Qt
import keyboard
from PySide6.QtCore import Signal

def empty_func():
    print("")

class ChatOverlay(QMainWindow):

    screenshot_signal = Signal()

    def __init__(self):
        super().__init__()
        self.callback_user_message_trigger = empty_func
        self.messages = []  # List to store messages
        self.init_ui()

    def init_ui(self):
        # Set up the main window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(100, 100, 400, 600)  # Example size

        # Load styles from CSS file
        with open("styles.qss", "r") as f:
            self.setStyleSheet(f.read())

        # Central widget setup
        central_widget = QWidget(self)
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Chat display area
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setObjectName("chatDisplay")
        layout.addWidget(self.chat_display)

        # Chat input area
        self.chat_input = QLineEdit(self)
        self.chat_input.setPlaceholderText("Type a message...")
        self.chat_input.setObjectName("chatInput")
        self.chat_input.returnPressed.connect(self.handle_user_message)
        layout.addWidget(self.chat_input)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        self.screenshot_signal.connect(self.update_chat_display)

    def handle_user_message(self):
        # Add the typed message to the messages list and update the display
        message = self.chat_input.text().strip()
        if message:
            self.add_message(f"Me: {message}")
        self.chat_input.clear()
        self.callback_user_message_trigger(self)

    def add_message(self, message: str):
        """ 
        Add a message to the chat and update the display.

        Args:
            message (str): The message to add.
        """
        self.messages.append(message)  # Add to the message list
        self.update_chat_display()

    def update_chat_display(self):
        """Update the chat display with all messages."""
        self.chat_display.clear()
        self.chat_display.append("<br>".join(self.messages))

    def get_message_list(self):
        """
        Get the list of messages stored in the chat.

        Returns:
            list: A list of message strings.
        """
        return self.messages

    def get_concatenated_messages(self):
        """
        Concatenate all messages into one string with newlines separating them.

        Returns:
            str: A single string with all messages separated by newlines.
        """
        return "\n".join(self.messages)

    def toggle_visibility(self):
        """Toggle the visibility of the window."""
        if self.isVisible():
            self.hide()
        else:
            self.show()
    
            # Enable mouse tracking for resizing
        self.setMouseTracking(True)
        self._is_dragging = False
        self._drag_start_position = None
        self._resize_start_position = None
        self._resizing = False
        self._resize_margin = 10  # Margin in pixels for detecting resize
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._is_in_resize_area(event.pos()):
                self._resizing = True
                self._resize_start_position = event.globalPos()
                self._start_geometry = self.geometry()
            else:
                self._is_dragging = True
                self._drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._resizing:
            # Handle resizing
            delta = event.globalPos() - self._resize_start_position
            new_rect = self._start_geometry.adjusted(0, 0, delta.x(), delta.y())
            self.setGeometry(new_rect)
        elif self._is_dragging:
            # Handle dragging
            self.move(event.globalPos() - self._drag_start_position)
        elif self._is_in_resize_area(event.pos()):
            # Update cursor if in resize area
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._is_dragging = False
            self._resizing = False
        super().mouseReleaseEvent(event)

    def _is_in_resize_area(self, pos):
        """Check if the mouse position is in the resize margin."""
        rect = self.rect()
        return rect.right() - self._resize_margin <= pos.x() <= rect.right() and \
               rect.bottom() - self._resize_margin <= pos.y() <= rect.bottom()