class PageAttr:
    """
    페이징 처리를 위한 속성과 계산 메서드를 제공하는 클래스입니다.

    Attributes:
        total_item_count (int): 전체 아이템의 수입니다.
        page_size (int): 한 페이지에 표시할 아이템의 수입니다. 기본값은 10입니다.
        current_page_number (int): 현재 페이지 번호입니다. 기본값은 1입니다.
        page_number_size (int): 한 번에 표시할 페이지 번호의 개수입니다. 기본값은 10입니다.
        offset (int): 현재 페이지의 시작 아이템의 인덱스입니다.
        limit (int): 한 페이지에 표시할 아이템의 최대 수입니다.
        total_page_count (int): 전체 페이지의 수입니다.
        start_page_number (int): 표시할 페이지 번호의 시작점입니다.
        end_page_number (int): 표시할 페이지 번호의 끝점입니다.
        is_exist_prev_page_number (bool): 이전 페이지가 존재하는지 여부입니다.
        is_exist_next_page_number (bool): 다음 페이지가 존재하는지 여부입니다.

    Methods:
        calculate(): 페이지네이션 관련 속성을 계산합니다.
    """    
    def __init__(self, total_item_count, page_size=10, current_page_number=1):
        self.total_item_count = total_item_count
        self.page_size = page_size
        self.current_page_number = current_page_number
        self.page_number_size = 10  # 한 번에 표시할 페이지 번호의 개수

        # 초기값 설정
        self.offset = 0
        self.limit = self.page_size
        self.total_page_count = 0
        self.start_page_number = 0
        self.end_page_number = 0
        self.is_exist_prev_page_number = False
        self.is_exist_next_page_number = False

        # 계산 메소드 실행
        self.calculate()

    def calculate(self):
        # 총 페이지 수 계산
        self.total_page_count = -(-self.total_item_count // self.page_size)  # 올림 계산

        # 현재 페이지 번호 검증
        self.current_page_number = max(1, min(self.current_page_number, self.total_page_count))

        # offset, limit 설정
        self.offset = (self.current_page_number - 1) * self.page_size
        self.limit = self.page_size

        # 시작 페이지 번호와 끝 페이지 번호 계산
        self.start_page_number = (self.current_page_number - 1) // self.page_number_size * self.page_number_size + 1
        self.end_page_number = min(self.start_page_number + self.page_number_size - 1, self.total_page_count)

        # 이전/다음 페이지 존재 여부
        self.is_exist_prev_page_number = self.current_page_number > 1
        self.is_exist_next_page_number = self.current_page_number < self.total_page_count


    def to_json(self):
        """
        인스턴스의 현재 상태를 나타내는 딕셔너리를 반환합니다.
        
        Returns:
            dict: 페이지네이션 정보가 담긴 딕셔너리.
        """
        return {
            "total_item_count": self.total_item_count,
            "page_size": self.page_size,
            "current_page_number": self.current_page_number,
            "total_page_count": self.total_page_count,
            "start_page_number": self.start_page_number,
            "end_page_number": self.end_page_number,
            "is_exist_prev_page_number": self.is_exist_prev_page_number,
            "is_exist_next_page_number": self.is_exist_next_page_number
        }