import sys
import sqlite3

from PySide6.QtCore import QSize, QDateTime
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QDateEdit
)


class NewTaskWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(220, 150))
        self.setWindowTitle("New Task")

        layout = QVBoxLayout()

        text_layout = QHBoxLayout()
        text_label = QLabel("text: ")
        text_label.setFixedWidth(40)
        text_layout.addWidget(text_label)
        self.text_edit = QLineEdit()
        self.text_edit.setFixedWidth(150)
        text_layout.addWidget(self.text_edit)
        layout.addLayout(text_layout)

        date_layout = QHBoxLayout()
        date_label = QLabel("date: ")
        date_label.setFixedWidth(40)
        date_layout.addWidget(date_label)
        self.date_edit = QDateEdit(calendarPopup=True)
        self.date_edit.setDateTime(QDateTime.currentDateTime())
        self.date_edit.setFixedWidth(150)
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_task(self):
        text = self.text_edit.text().strip()
        date = self.date_edit.date()
        formatted_date = f"{date.year()}-{date.month()}-{date.day()}"

        if text == "":
            return

        conn.execute(f"INSERT INTO tasks (text, date) VALUES ('{text}', '{formatted_date}')")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(200, 50))
        self.setWindowTitle("To Do List")
        self.newTaskWindow = NewTaskWindow()

        layout = QVBoxLayout()

        self.button = QPushButton("New Task")
        self.button.clicked.connect(self.new_task)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def new_task(self):
        if self.newTaskWindow.isVisible():
            self.newTaskWindow.hide()
        else:
            self.newTaskWindow.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    conn = sqlite3.connect("tasks.db")
    conn.execute("CREATE TABLE IF NOT EXISTS tasks(text TEXT, date TEXT)")
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
