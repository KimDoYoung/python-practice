# ChartRequest.py
from pydantic import BaseModel, Field
from typing import List
from typing import List, Tuple, Optional


class ChartBase(BaseModel):
    user_id: str
    result_type: str = 'url'  # url과 stream 두 가지
    chart_type: str
    width: int = 800
    height: int = 600
    title: Optional[str] = None

class LineChartRequest(ChartBase):
    chart_type: str = 'line'
    x_data: List[float]
    y_data: List[List[float]]
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    line_colors: Optional[List[str]] = None
    line_styles: Optional[List[str]] = None
    line_widths: Optional[List[float]] = None
    legend_labels: Optional[List[str]] = None
    axis_range: Optional[List[Tuple[float, float]]] = None
    marker_styles: Optional[List[str]] = None
    grid: Optional[bool] = None
    text_labels: Optional[List[List[Tuple[float, float, str]]]] = None

class BarChartRequest(ChartBase):
    chart_type: str = 'bar'
    x_data: List[float]
    y_data: List[List[float]]
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    bar_colors: Optional[List[str]] = None  # 바 차트에 특화된 속성
    bar_widths: Optional[List[float]] = None  # 바 너비를 추가할 수 있음
    legend_labels: Optional[List[str]] = None
    axis_range: Optional[List[Tuple[float, float]]] = None
    grid: Optional[bool] = None

class PieChartRequest(ChartBase):
    chart_type: str = 'pie'
    labels: List[str] = Field(...)  # 파이차트의 각 섹션을 나타내는 레이블 목록
    sizes: List[int] = Field(...)  # 각 레이블의 값(크기)을 나타내는 목록, 파이차트에서의 비율을 결정
    colors: List[str] = Field(...)  # 파이차트의 각 섹션에 적용될 색상 목록
    explode: List[float] = Field(default_factory=lambda: [0.0 for _ in range(len(self.labels))])  # 특정 섹션을 중심에서 돌출시키는 값의 목록
    shadow: Optional[bool] = False  # 파이차트에 그림자 표시 여부
    startangle: Optional[int] = 90  # 파이차트의 시작 각도
    autopct: Optional[str] = "%1.1f%%"  # 파이차트의 각 섹션에 표시될 비율의 문자열 포맷
    pctdistance: Optional[float] = 0.85  # 비율 텍스트가 중심에서 떨어진 거리 (반지름 대비 비율)
    labeldistance: Optional[float] = 1.1  # 레이블이 중심에서 떨어진 거리 (반지름 대비 비율)
    wedgeprops: Optional[dict] = Field(default_factory=lambda: {"linewidth": 1, "edgecolor": "black"})  # 파이 섹션 스타일 설정 (예: 테두리 두께, 색상)
    textprops: Optional[dict] = Field(default_factory=lambda: {"fontsize": 12})  # 텍스트 스타일 설정 (예: 폰트 크기)
    radius: Optional[float] = 1.0  # 파이차트의 반지름
    counterclock: Optional[bool] = False  # 파이차트의 조각들을 시계 반대 방향으로 배치할지 여부
    frame: Optional[bool] = False  # 차트 주변에 프레임 표시 여부
    legend_labels: Optional[List[str]] = None  # 범례 레이블 목록 (추가됨)
    legend_loc: Optional[str] = 'best'  # 범례의 위치를 지정하는 속성 추가


# sample table을 위한 class
class ChartSampleRequest(BaseModel):
    # id : int
    chart_type: str
    title: str
    json_data: str
    note: str