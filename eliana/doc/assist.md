# chatGPT로 부터 얻은 자료

## 선그래프를 위한 데이터들

```python
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional

class LineGraphData(BaseModel):
    title: Optional[str] = Field(None, description="The title of the graph.")
    x_data: List[float] = Field(..., description="The data points for the x-axis.")
    y_data: List[float] = Field(..., description="The data points for the y-axis.")
    x_label: Optional[str] = Field(None, description="Label for the x-axis.")
    y_label: Optional[str] = Field(None, description="Label for the y-axis.")
    line_color: Optional[str] = Field(None, description="Color of the line.")
    line_style: Optional[str] = Field(None, description="Style of the line.")
    line_width: Optional[float] = Field(None, description="Width of the line.")
    legend_label: Optional[str] = Field(None, description="Label for the legend.")
    axis_range: Optional[Tuple[Tuple[float, float], Tuple[float, float]]] = Field(None, description="Range for the x and y axes.")
    marker_style: Optional[str] = Field(None, description="Style of the markers.")
    grid: Optional[bool] = Field(None, description="Whether to show grid lines.")
    text_labels: Optional[List[Tuple[float, float, str]]] = Field(None, description="Text labels for specific points.")
```

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = FastAPI()

class LineGraphData(BaseModel):
    x_data: List[float]
    y_data: List[float]
    title: Optional[str] = None
    x_label: Optional[str] = None
    y_label: Optional[str] = None
    line_color: Optional[str] = None
    line_style: Optional[str] = None
    line_width: Optional[float] = None
    legend_label: Optional[str] = None
    axis_range: Optional[Tuple[Tuple[float, float], Tuple[float, float]]] = None
    marker_style: Optional[str] = None
    grid: Optional[bool] = None
    text_labels: Optional[List[Tuple[float, float, str]]] = None

@app.post("/create_chart")
def create_chart(request: LineGraphData):
    plt.figure()
    plt.plot(request.x_data, request.y_data, label=request.legend_label, color=request.line_color, linestyle=request.line_style, linewidth=request.line_width, marker=request.marker_style)
    
    if request.title:
        plt.title(request.title)
    if request.x_label:
        plt.xlabel(request.x_label)
    if request.y_label:
        plt.ylabel(request.y_label)
    if request.grid:
        plt.grid(request.grid)
    if request.axis_range:
        plt.xlim(request.axis_range[0])
        plt.ylim(request.axis_range[1])
    if request.text_labels:
        for x, y, label in request.text_labels:
            plt.text(x, y, label)
    
    plt.legend()

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    
    html_content = f'<img src="data:image/png;base64, {img_base64}" alt="Line Graph">'
    return HTMLResponse(content=html_content, status_code=200)

```

### 라인 그리는 json data
```json
{
    "title": "Example Line Graph",
    "x_data": [
        1.0,
        2.0,
        3.0,
        4.0,
        5.0
    ],
    "y_data": [
        [
            2.0,
            4.0,
            6.0,
            8.0,
            10.0
        ],
        [
            3.0,
            6.0,
            9.0,
            12.0,
            15.0
        ]
    ],
    "x_label": "X-axis",
    "y_label": "Y-axis",
    "line_colors": [
        "blue",
        "red"
    ],
    "line_styles": [
        "solid",
        "dashed"
    ],
    "line_widths": [
        2.0,
        1.5
    ],
    "legend_labels": [
        "Data 1",
        "Data 2"
    ],
    "axis_range": [
        [
            0.0,
            6.0
        ],
        [
            0.0,
            16.0
        ]
    ],
    "marker_styles": [
        "circle",
        "triangle"
    ],
    "grid": true,
    "text_labels": [
        [
            [
                2.0,
                4.0,
                "Point 2, 4"
            ],
            [
                4.0,
                8.0,
                "Point 4, 8"
            ]
        ],
        [
            [
                2.0,
                6.0,
                "Point 2, 6"
            ],
            [
                4.0,
                12.0,
                "Point 4, 12"
            ]
        ]
    ]
}

```

## router

```python
# routers/item.py

from fastapi import APIRouter
from models import Item

router = APIRouter()

@router.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@router.post("/items/")
async def create_item(item: Item):
    return item.dict()


# main.py

from fastapi import FastAPI
from routers import user, item

app = FastAPI()

app.include_router(user.router)
app.include_router(item.router)

```

### 샘플 코드
```
# @app.post("/test")
# def create_chart(request: ChartRequest):
#     # 파일 경로 생성
#     file_path = get_file_path(request.width, request.height)

#     # 현재 파일의 디렉토리 경로를 구함
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     print(current_dir)

#     # fonts 폴더 내의 폰트 파일 경로를 구성
#     font_path = os.path.join(current_dir, 'assets', 'fonts', 'NanumGothic.ttf')  # 'NanumGothic.ttf'를 예로 들었습니다.

#     # 한글 폰트 설정
#     # font_name = fm.FontProperties(fname=font_path).get_name()
#     # plt.rc('font', family=font_name)
#     # 폰트 매니저에 경로 추가
#     fm.fontManager.addfont(font_path)

#     # 폰트 설정
#     plt.rcParams['font.family'] = 'NanumGothic'

#     # 차트 생성 및 파일로 저장
#     plt.figure(figsize=(request.width / 100, request.height / 100))
#     plt.plot(request.x, request.y)
#     plt.title("샘플챠트")
#     plt.savefig(file_path)
#     plt.close()

#     # 생성된 이미지 파일의 URL 반환
#     # 여기서는 예시로 localhost를 사용하고 있으나, 실제 배포 환경에 맞게 수정해야 합니다.
#     url = f"http://localhost:8989/{file_path}"
#     return {"url": url}
```
