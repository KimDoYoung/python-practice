--------------------------------------------
JSON data
var json_data = {
    "user_id": "kdy987",
    "result_type": "url",
    "chart_type": "bar",
    "width": 800,
    "height": 600,
    "title": "Line Chart 샘플",
    "x_data": [1, 2, 3, 4, 5, 7],
    "y_data": [[5, 7, 3, 8, 9], [2, 4, 6, 1, 3]],
    "x_label": "X 축 라벨",
    "y_label": "Y 축 라벨",
    "bar_colors": ["blue", "green"],
    "bar_widths": [0.4, 0.4],
    "legend_labels": ["데이터 시리즈 1", "데이터 시리즈 2"],
    "axis_range": [[0, 6], [0, 10]],
    "grid": true
};
------------------------------------------------
Request
class ChartBase(BaseModel):
    user_id: str
    result_type: str = 'url'  # url과 stream 두 가지
    chart_type: str
    width: int = 800
    height: int = 600
    title: Optional[str] = None

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
-------------------------------------------------
chart make logic
def create_bar_chart(request):
            
    # 파일 경로 생성
    file_path = get_file_path(request.width, request.height)

    # 차트 생성 로직 (matplotlib 사용)
    plt.figure(figsize=(request.width / 100, request.height / 100))

    if request.title:
        plt.title(request.title)
    if request.x_label:
        plt.xlabel(request.x_label)
    if request.y_label:
        plt.ylabel(request.y_label)
    if request.grid:
        plt.grid(request.grid)

    # 바 차트 그리기
    for i, y_data in enumerate(request.y_data):
        plt.bar(request.x_data, y_data, 
                color=request.bar_colors[i] if request.bar_colors else None,
                width=request.bar_widths[i] if request.bar_widths else None,
                label=request.legend_labels[i] if request.legend_labels else None)

    # 축 범위 설정
    if request.axis_range:
        plt.xlim(request.axis_range[0])
        plt.ylim(request.axis_range[1])

    # 범례 추가
    if request.legend_labels:
        plt.legend()

    plt.savefig(file_path)
    plt.close()

    # 생성된 이미지 파일의 URL 반환
    return f"{CHART_BASE_URL}/{file_path}"
----------------------------------------------
1. 위와 같이 bar chart 이미지를 만드는 필요한 소스 3가지 입니다.
2. JSON 데이터를 Request 클래스로 받아서 create_bar_chart  함수에서 bar chart 이미지를 만듭니다.
3. 위의 3가지 소스를 참조하여 client 에서 javascript(jquery사용) JSON data에 대해서 validation 검증 코드를 만들어 줄 수 있을까요?
4. 에러 메세지는 한글로 해주세요.
5. user_id는 필수여야합니다.
6. result_type은 'url'   또는 'stream'  이어야하며 필수 입니다.
var json_data = {...}
var errors = validation_bar_chart_data(json_data){
    var errors =[];
    //이 부분 코드 생성
    return errors;
}
