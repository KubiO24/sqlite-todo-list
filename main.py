import sys
import sqlite3
from functools import partial
from datetime import date, datetime

from PySide6.QtCore import QSize, QDateTime, Qt
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QDateEdit, QFrame, QGraphicsDropShadowEffect,
    QDateTimeEdit
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
        self.date_edit = QDateTimeEdit(calendarPopup=True)
        self.date_edit.setDateTime(datetime.today())
        self.date_edit.setFixedWidth(150)
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_task)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def add_task(self):
        task_text = self.text_edit.text().strip()
        task_date = self.date_edit.dateTime()
        formatted_date = task_date.toString("yyyy-MM-dd HH:mm")

        if task_text == "":
            return

        conn.execute(f"INSERT INTO tasks (text, date, is_done) VALUES ('{task_text}', '{formatted_date}', '0')")
        conn.commit()
        refresh_tasks()

        self.close()

class EditTaskWindow(QWidget):
    def __init__(self, old_task_text, old_task_date):
        super().__init__()

        self.old_task_text = old_task_text
        self.old_task_date = old_task_date

        self.setFixedSize(QSize(220, 150))
        self.setWindowTitle("Edit Task")

        layout = QVBoxLayout()

        text_layout = QHBoxLayout()
        text_label = QLabel("text: ")
        text_label.setFixedWidth(40)
        text_layout.addWidget(text_label)
        self.text_edit = QLineEdit(self.old_task_text)
        self.text_edit.setFixedWidth(150)
        text_layout.addWidget(self.text_edit)
        layout.addLayout(text_layout)

        date_layout = QHBoxLayout()
        date_label = QLabel("date: ")
        date_label.setFixedWidth(40)
        date_layout.addWidget(date_label)
        self.date_edit = QDateTimeEdit(calendarPopup=True)
        self.date_edit.setDateTime(datetime.strptime(self.old_task_date, "%Y-%m-%d %H:%M"))
        self.date_edit.setFixedWidth(150)
        date_layout.addWidget(self.date_edit)
        layout.addLayout(date_layout)

        self.add_button = QPushButton("Save")
        self.add_button.clicked.connect(self.save_task)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def save_task(self):
        task_text = self.text_edit.text().strip()
        task_date = self.date_edit.dateTime()
        formatted_date = task_date.toString("yyyy-MM-dd HH:mm")

        if task_text == "":
            return

        conn.execute(f"UPDATE tasks SET text='{task_text}', date='{formatted_date}' WHERE text='{self.old_task_text}' AND date='{self.old_task_date}' AND is_done='0'")
        conn.commit()
        refresh_tasks()

        self.close()


class MainWindow(QMainWindow):
    task_list = QVBoxLayout()

    def __init__(self):
        super().__init__()

        self.setFixedWidth(400)
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
        child.widget().deleteLater()

    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks ORDER BY is_done DESC, date ASC")
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
        task_text = row[0]
        task_date = row[1]
        task_is_done = row[2]
        task_date_format = datetime.strptime(task_date, "%Y-%m-%d %H:%M")

        task_container = QWidget()
        if task_is_done:
            task_container.setObjectName("container_done")
        elif task_date_format < datetime.today():
            task_container.setObjectName("container_expired")
        elif task_date_format == date.today():
            task_container.setObjectName("container_today")
        else:
            task_container.setObjectName("container")
        task_container.setMaximumHeight(30)
        task_container.setStyleSheet("""
            QWidget#container {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 5px;
            }
            
            QWidget#container_expired {
                background-color: rgba(255, 0, 0, 0.15);
                border-radius: 5px;
            }
            
            QWidget#container_today {
                background-color: rgba(255, 190, 0, 0.15);
                border-radius: 5px;
            }
            
            QWidget#container_done {
                background-color: rgba(0, 255, 0, 0.15);
                border-radius: 5px;
            }
            
            QLabel#text {
                font-weight: bold;
            }
            
            QLabel#date {
                color: rgb(50, 50, 50);
            }
            
            QPushButton#edit_button {
                font-size: 12px;
                border: none;
                font-weight: bold;
                color: rgb(0, 0, 220);
            }
            
            QPushButton#edit_button:hover {
                color: rgb(0, 0, 170);
            }
            
            QPushButton#done_button {
                font-size: 15px;
                border: none;
                font-weight: bold;
                color: rgb(0, 220, 0);
            }
            
            QPushButton#done_button:hover {
                color: rgb(0, 170, 0);
            }
            
            QPushButton#delete_button {
                font-size: 15px;
                border: none;
                font-weight: bold;
                color: red;
            }
            
            QPushButton#delete_button:hover {
                color: rgb(200, 0, 0);
            }
        """)

        task_layout = QHBoxLayout(task_container)
        MainWindow.task_list.addWidget(task_container)

        task_text_label = QLabel(task_text)
        task_text_label.setFixedWidth(150)
        task_text_label.setObjectName("text")
        task_layout.addWidget(task_text_label)


        task_date_label = QLabel(task_date)
        task_date_label.setFixedWidth(90)
        task_date_label.setObjectName("date")
        task_layout.addWidget(task_date_label)

        task_layout.addStretch()

        if not task_is_done:
            edit_button = QPushButton("Edit")
            edit_button.setObjectName("edit_button")
            edit_button.setFixedWidth(20)
            edit_button.clicked.connect(partial(edit_task, task_text, task_date))
            task_layout.addWidget(edit_button)

            done_button = QPushButton("✓")
            done_button.setObjectName("done_button")
            done_button.setFixedWidth(15)
            done_button.clicked.connect(partial(done_task, task_text, task_date, task_is_done))
            task_layout.addWidget(done_button)


        delete_button = QPushButton("X")
        delete_button.setObjectName("delete_button")
        delete_button.setFixedWidth(15)
        delete_button.clicked.connect(partial(delete_task, task_text, task_date, task_is_done))
        task_layout.addWidget(delete_button)


def done_task(task_text, task_date, task_is_done):
    conn.execute(f"UPDATE tasks SET is_done='1' WHERE text='{task_text}' AND date='{task_date}' AND is_done='{task_is_done}'")
    conn.commit()
    refresh_tasks()
    return

def delete_task(task_text, task_date, task_is_done):
    conn.execute(f"DELETE FROM tasks WHERE text='{task_text}' AND date='{task_date}' AND is_done='{task_is_done}'")
    conn.commit()
    refresh_tasks()
    return

def edit_task(task_text, task_date):
    w.editTaskWindow = EditTaskWindow(task_text, task_date)
    w.editTaskWindow.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    conn = sqlite3.connect("tasks.db")
    conn.execute("CREATE TABLE IF NOT EXISTS tasks(text TEXT, date TEXT, is_done BOOLEAN)")
    w = MainWindow()
    w.show()
    refresh_tasks()
    sys.exit(app.exec())
