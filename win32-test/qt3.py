import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel('Hello, PyQt5!', self)
        self.label.setAlignment(Qt.AlignCenter)

        self.btn = QPushButton('Click me!', self)
        self.btn.clicked.connect(self.changeText)

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.btn)

        self.setLayout(vbox)

        self.setWindowTitle('Simple PyQt5 App')
        self.setGeometry(300, 300, 300, 200)  # 위치 x, y, 너비, 높이
        self.show()

    def changeText(self):
        self.label.setText('Button clicked!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
