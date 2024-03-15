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
    data: List[float]  # 파이 차트의 각 조각에 해당하는 데이터
    labels: List[str]  # 각 데이터 조각의 라벨
    colors: Optional[List[str]] = None  # 파이 차트 조각의 색상 (선택 사항)
    explode: Optional[List[float]] = None  # 파이 차트의 조각을 돌출시키는 정도 (선택 사항)
    startangle: Optional[float] = 140  # 파이 차트 시작 각도 (선택 사항)
    autopct: Optional[str] = '%1.1f%%'  # 파이 조각의 백분율 표시 형식 (선택 사항)

# sample table을 위한 class
class ChartSampleRequest(BaseModel):
    # id : int
    chart_type: str
    title: str
    json_data: str
    note: str