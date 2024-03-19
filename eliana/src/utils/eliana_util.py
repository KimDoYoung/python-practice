# 차트 타입에 따라 요청 클래스 매핑
from typing import Dict
from fastapi import HTTPException
from pydantic import ValidationError
from model.ChartRequest import BarChartRequest, ChartBase, LineChartRequest, PieChartRequest
from utils.charts_util import create_bar_chart, create_line_chart
from model.ChartRequest import BarChartRequest, LineChartRequest, PieChartRequest
from utils.charts_util import create_bar_chart, create_line_chart


chart_type_to_class = {
    "line": LineChartRequest,
    "bar": BarChartRequest,
    "pie": PieChartRequest,
}

# 챠트 그리를 함수들
chart_creator = {
    "line": create_line_chart,
    "bar": create_bar_chart
}


def chartTypeName(chart_type):
    names = {'line' : "라인", 'bar' : "막대"}
    return names[chart_type]

def get_chart_request(request: Dict) -> ChartBase:
    chart_type = request.get("chart_type")
    chart_class = chart_type_to_class[chart_type]
    if not chart_class:
        raise HTTPException(status_code=400, detail=f"Unsupported chart type: {chart_type}")
    try:
        return chart_class(**request)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error for {chart_type} chart: {e}")