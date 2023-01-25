import sys
import sqlite3
from new_task_window import NewTaskWindow

from PySide6.QtCore import QSize, QDateTime
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QDateEdit
)


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
