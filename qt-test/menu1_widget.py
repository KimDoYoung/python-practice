from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QMessageBox

class Menu1Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        grid = QGridLayout()
        

        grid.addWidget(QLabel("Title:"), 0, 0)
        grid.addWidget(QLabel("Author:"), 1, 0)
        grid.addWidget(QLabel("Review:"), 2,0)

        grid.addWidget(QLineEdit(), 0, 1)
        grid.addWidget(QLineEdit(), 1, 1)
        grid.addWidget(QTextEdit(), 2, 1)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save)
        buttonLayout.addWidget(save_button)

        layout.addLayout(grid)
        layout.addLayout(buttonLayout)

        self.setLayout(layout)

    def save(self):
        reply = QMessageBox.question(self, 'Message', 'Do you want to save?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, 'Message', 'Saved', QMessageBox.Ok, QMessageBox.Ok)
        
