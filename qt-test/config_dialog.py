from PyQt5.QtWidgets import QDialog, QPushButton, QVBoxLayout

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.centerOnParent()

    def initUI(self):
        self.setWindowTitle('Config')
        self.setGeometry(100, 100, 600, 400)
        close_button = QPushButton('닫기', self)
        close_button.clicked.connect(self.close)
        
        layout = QVBoxLayout()
        layout.addWidget(close_button)
        self.setLayout(layout)

    def centerOnParent(self):
        parent_geometry = self.parent().geometry()
        self_geometry = self.frameGeometry()
        center_point = parent_geometry.center()
        self_geometry.moveCenter(center_point)
        self.move(self_geometry.topLeft())