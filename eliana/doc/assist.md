# chatGPT로 부터 얻은 자료

## 선그래프를 위한 데이터들

```python
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional

class LineGraphData(BaseModel):
    x_data: List[float] = Field(..., description="The data points for the x-axis.")
    y_data: List[float] = Field(..., description="The data points for the y-axis.")
    title: Optional[str] = Field(None, description="The title of the graph.")
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