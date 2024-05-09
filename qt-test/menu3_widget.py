from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class Menu3Widget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("This is the content of Menu 3")
        layout.addWidget(label)
        self.setLayout(layout)
