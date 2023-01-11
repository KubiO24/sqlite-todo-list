import sys

from PySide6.QtCore import QSize
from PySide6.QtWidgets import (
    QApplication, QLabel, QMainWindow,
    QPushButton, QVBoxLayout, QWidget
)


class NewTaskWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("New Task Window")
        layout.addWidget(self.label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(400, 300))
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


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()
app.exec()
