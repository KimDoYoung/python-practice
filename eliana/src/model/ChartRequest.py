# ChartRequest.py
from pydantic import BaseModel
from typing import List
from typing import List, Tuple, Optional

class ChartBase(BaseModel):
    result_type: str = 'url' # url과 stream  두가지 
    chart_type: str = 'line' # line, bar ...
    width: int = 800
    height: int = 600


class LineBarRequest(ChartBase):
    title: Optional[str] = None  # 그래프의 제목입니다.
    x_data: List[float]          # x 축의 데이터 포인트입니다.
    y_data: List[List[float]]    # y 축의 데이터 포인트입니다.
    x_label: Optional[str] = None  # x 축의 라벨입니다.
    y_label: Optional[str] = None  # y 축의 라벨입니다.
    line_colors: Optional[List[str]] = None  # 선의 색상입니다.
    line_styles: Optional[List[str]] = None  # 선의 스타일입니다.
    line_widths: Optional[List[float]] = None  # 선의 너비입니다.
    legend_labels: Optional[List[str]] = None  # 범례의 라벨입니다.
    axis_range: Optional[List[Tuple[float, float]]] = None  # x 및 y 축의 범위입니다.
    marker_styles: Optional[List[str]] = None  # 마커의 스타일입니다.
    grid: Optional[bool] = None  # 격자선을 표시할지 여부입니다.
    text_labels: Optional[List[List[Tuple[float, float, str]]]] = None  # 특정 점에 대한 텍스트 라벨입니다.
