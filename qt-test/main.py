import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QAction, qApp, QVBoxLayout, QPushButton, 
                            QHBoxLayout, QWidget, QSplitter, QTabWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDesktopWidget, QDialog
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
from config_dialog import ConfigDialog
from PyQt5.QtWidgets import QLabel
from closeable_tab_widget import CloseableTabWidget

class ExampleApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowIcon(QIcon('orange.ico'))
        self.setWindowTitle('Qt5 UI 예제')
        self.setGeometry(100, 100, 1400, 900)

        # 메뉴 바 설정
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        configAction = QAction('&Config', self)
        configAction.triggered.connect(self.openConfigDialog)
        quitAction = QAction('&Quit', self)
        quitAction.setShortcut('Ctrl+Q')
        quitAction.triggered.connect(self.close)

        fileMenu.addAction(configAction)
        fileMenu.addAction(quitAction)

        # 스플리터 설정
        splitter = QSplitter(Qt.Horizontal)

        left_panel = QWidget()
        right_panel = QWidget()
        left_panel.setStyleSheet("background-color: lightblue;") 
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([200, 1200])

        # 왼쪽 패널 버튼 추가
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignTop) 
        buttons = ['menu1', 'menu2', 'menu3']
        for btn in buttons:
            button = QPushButton(btn, self)
            button.setToolTip("This is a <b>QPushButton</b> widget") # 툴팁 추가
            button.clicked.connect(lambda _, name=btn: self.handleMenuClick(name))  
            vbox.addWidget(button)
        left_panel.setLayout(vbox)

        self.tabs = {}
        # 오른쪽 패널 탭 추가
        self.tab_widget = CloseableTabWidget(self)
        
        right_panel.setLayout(QVBoxLayout())
        right_panel.layout().addWidget(self.tab_widget)

        self.setCentralWidget(splitter)

        # 상태 표시줄 추가
        self.displayMessage("Ready....")

        self.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def displayMessage(self, message:str):
        self.date = QDate.currentDate()
        msg = self.date.toString(Qt.DefaultLocaleLongDate) + " | " + message
        self.statusBar().showMessage(msg)

    def openConfigDialog(self):
        dialog = ConfigDialog(self)
        dialog.exec_()        

    # 'Quit' 메뉴 액션에 연결할 새로운 메서드
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "종료하시겠습니까?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def handleMenuClick(self, name):
        if name not in self.tabs:
            # 탭 생성
            tab = QWidget()
            layout = QVBoxLayout()
            label = QLabel(f'Content for {name}')
            layout.addWidget(label)
            tab.setLayout(layout)
            idx = self.tab_widget.addTab(tab, name)
            self.tabs[name] = idx
        # 탭 활성화
        self.tab_widget.setCurrentIndex(self.tabs[name])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExampleApp()
    ex.show()
    sys.exit(app.exec_())
