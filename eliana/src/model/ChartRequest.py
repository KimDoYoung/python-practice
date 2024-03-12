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

class ChartSampleRequest(BaseModel):
    chart_type: str
    title: str
    #data_json: str = Field(..., alias="json")  # `json` 대신 `data_json` 사용
    json: str
    note: str