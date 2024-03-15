
```

@router.post("/chart/bar")
async def chart_bar(request: BarChartRequest, db: Session = Depends(get_db)):
    logger.debug(f"/chart/bar start : {request}")
    # hash를 구해서 
    request_hash = calculate_request_hash(request);
    chart_history = db.query(ChartHistory).filter(ChartHistory.json_hash == request_hash).first()

    # 존재하면 url을 리턴
    if chart_history:
        logger.debug(f"already exists in chart_history table : {request_hash}")
        return {"url": chart_history.url}
        
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
    url = f"http://localhost:8989/{file_path}"


    # db에 저장   
    request_json = json.dumps(vars(request), indent=2)
    new_chart_history = ChartHistory(user_id= request.user_id, chart_type=request.chart_type,json_data=request_json, json_hash= request_hash, url=url )
    add_chart_history(new_chart_history)

    return {"url": url, "title": request.title}
```    
막대그래프를 이미지 파일로 만드는 controller입니다. 좀 더 나은 코드로 만들고 싶어요. 어떻게 수정하면 좋을까요?




# chart_utils.py
def create_bar_chart(request, file_path):
    # 차트 생성 로직...
    return file_path

def save_chart_history(db, request, url):
    # 데이터베이스 저장 로직...
    pass

# constants.py
CHART_BASE_URL = "http://localhost:8989/"

# chart_controller.py
from chart_utils import create_bar_chart, save_chart_history
from constants import CHART_BASE_URL

@router.post("/chart/bar")
async def chart_bar(request: BarChartRequest, db: Session = Depends(get_db)):
    # 기능별 로직 분리...
    chart_url = CHART_BASE_URL + file_path
    save_chart_history(db, request, chart_url)
    return {"url": chart_url, "title": request.title}
