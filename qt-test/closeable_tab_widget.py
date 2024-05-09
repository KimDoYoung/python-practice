from PyQt5.QtWidgets import QTabWidget


class CloseableTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setTabsClosable(True)  # 모든 탭에 닫기 버튼 활성화
        self.tabCloseRequested.connect(self.handleTabCloseRequested)  # 탭 닫기 요청 시그널에 슬롯 연결
    
    def handleTabCloseRequested(self, index):
        tab_name = self.tabText(index)  # 닫히는 탭의 이름을 가져옵니다.
        self.removeTab(index)  # 탭을 제거합니다.
        # 탭 이름을 사용하여 self.tabs 딕셔너리에서도 해당 항목을 제거합니다.
        if tab_name in self.parent.tabs:
            del self.parent.tabs[tab_name]

        # parent = self.parent()  # 부모 객체를 가져옵니다.
        # if parent and hasattr(parent, 'tabs') and tab_name in parent.tabs:
        #     del parent.tabs[tab_name]
        # else:
        #     print("Parent is not set correctly or 'tabs' attribute does not exist.")