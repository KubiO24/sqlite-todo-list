import sys
import sqlite3

from PySide6.QtCore import QSize, QDateTime, Qt
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QDateEdit, QFrame, QGraphicsDropShadowEffect
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

        refresh_tasks()

        self.close()


class MainWindow(QMainWindow):
    task_list = QVBoxLayout()

    def __init__(self):
        super().__init__()

        self.setFixedWidth(300)
        self.setWindowTitle("To Do List")
        self.newTaskWindow = NewTaskWindow()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setContentsMargins(0, 10, 0, 10) # left, top, right, bottom

        self.button = QPushButton("New Task")
        self.button.setFixedWidth(120)
        self.button.clicked.connect(self.new_task)

        button_layout.addWidget(self.button)
        layout.addLayout(button_layout)

        self.task_list.setContentsMargins(0, 0, 0, 10) # left, top, right, bottom
        layout.addLayout(self.task_list)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def new_task(self):
        if self.newTaskWindow.isVisible():
            self.newTaskWindow.hide()
        else:
            self.newTaskWindow.show()


def refresh_tasks():
    while (child := MainWindow.task_list.takeAt(0)) is not None:
        print(child.widget())
        child.widget().deleteLater()

    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")
    rows = cur.fetchall()

    if not rows:
        no_task_container = QWidget()
        no_task_layout = QHBoxLayout(no_task_container)
        MainWindow.task_list.addWidget(no_task_container)
        no_task_text = QLabel("Your to do list is empty.")
        no_task_text.setStyleSheet("color: rgb(100, 100, 100);")
        no_task_layout.addStretch()
        no_task_layout.addWidget(no_task_text)
        no_task_layout.addStretch()
        return

    for row in rows:
        task_container = QWidget()
        task_container.setObjectName("container")
        task_container.setMaximumHeight(30)
        task_container.setStyleSheet("""
            QWidget#container {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 5px;
            }
            
            QLabel#text {
                font-weight: bold;
            }
            
            QLabel#date {
                color: rgb(50, 50, 50);
            }
        """)

        task_layout = QHBoxLayout(task_container)
        MainWindow.task_list.addWidget(task_container)

        task_text = QLabel(row[0])
        task_text.setObjectName("text")
        task_layout.addWidget(task_text)
        task_layout.addStretch()

        task_date = QLabel(row[1])
        task_date.setObjectName("date")
        task_layout.addWidget(task_date)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    conn = sqlite3.connect("tasks.db")
    conn.execute("CREATE TABLE IF NOT EXISTS tasks(text TEXT, date TEXT)")
    w = MainWindow()
    w.show()
    refresh_tasks()
    sys.exit(app.exec())
