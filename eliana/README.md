# Eliana

## 개요

1. chart server
   1. 사용자로부터 chart를 그리는 데이터(json)를 받아서 그것으로 chart 이미지를 만들고 url 또는 stream을 리턴한다.
   2. 사용자는 화면에서 테스트 데이터로 만들어질 챠트를 확인하고.
   3. 자신이 작성하는 application에서 json데이터를 Eliana로 보내서 챠트 이미지를 만들게 하고 url또는 stream을 리턴받아서 표현한다.
   
2. 기술스택
   * FastAPI
   * Matplotlib
   * SqlLite
   * tailwind
  

## 개발환경

### 가상환경 설정
```
    python -m venv env
    . ./env/Scripts/activate
```

### 라이브러리 설치

```
pip install fastapi uvicorn
pip install matplotlib
pip install jinja2
pip install -e .

## pip관련 명령어
```
pip freeze > requirements.txt
pip install -r requirements.txt
pip install --upgrade fastapi httpx
pytest > ~/tmp/eliana_test_results.txt 2>&1
pytest -W ignore::DeprecationWarning
```

```
## 데이터베이스

* sqlite 를 사용 : eliana.db 

### 실행

```
ELIANA_MODE=local
uvicorn --app-dir src main:app --reload --port 8989
#uvicorn main:app --reload --port 8989
.env
uvicorn app:app --port $ELINA_PORT
```

## 환경설정

### .env
```
ELINA_MODE=LOCAL
```


 ### 테스트
 * pytest
 * swagger 
 ```
 http://localhost:8989/docs

{
  "type": "url",
  "width": 300,
  "height": 200,
  "x": ["2024-01","2024-02","2024-03","2024-04","2024-05"],
  "y": [23,45,53,32,65]
}
```

## 개발 내용

1. sqlite 사용
   - eliana.db : 같은 폴더에 생성
   - chart_history : 사용자가 생성한 chart history
   - chart_sample  : 챠트 샘플들 즉 구현된 챠트종류, 사용자는 이것을 수정해서 사용할 수 있다.
   
2. 환경변수 : ELIANA_MODE 사용
3. log폴더 안에 eliana.log 생성

## 새로은 챠트의 추가

1. 아래 line chart를 위한 클래스를  참조하여 pie챠트의 클래스를 만들어 주세요
```
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
```


## 폴더 구조
```
.vscode: Visual Studio Code 설정 파일이 저장되는 디렉토리입니다. 이 폴더에는 에디터 설정, 디버깅 구성 등 VS Code를 위한 설정 파일이 포함될 수 있습니다.

assets: 웹 프로젝트에서 사용되는 정적 자원들을 저장하는 디렉토리입니다. 이 안에는 css, fonts, image, js 등의 서브디렉토리가 있어, 각각 스타일시트, 폰트 파일, 이미지 파일, 자바스크립트 파일을 관리합니다.

charts: 생성된 차트 이미지 파일들을 저장하는 디렉토리입니다. 예를 들어 2024/03 같은 서브디렉토리 구조를 통해, 연도와 월별로 차트 이미지를 분류할 수 있습니다.

doc: 프로젝트 문서화 파일들을 저장하는 디렉토리입니다. 여기에는 프로젝트 설명, 사용 방법, API 문서 등이 포함될 수 있습니다.

env: Python 가상 환경 디렉토리입니다. 이 폴더에는 프로젝트를 위해 설치된 Python 인터프리터와 라이브러리가 포함됩니다. Lib/site-packages에는 프로젝트 의존성이 저장되어 있습니다.

log: 애플리케이션 로그 파일들을 저장하는 디렉토리입니다.

src: 소스 코드를 포함하는 주 디렉토리입니다. 이 안에는 FastAPI 애플리케이션의 실제 Python 코드가 포함되어 있으며, exception, model, routers, utils 등의 서브디렉토리로 구성될 수 있습니다. 각 디렉토리는 애플리케이션의 다른 부분을 담당합니다.

templates: Jinja2 같은 템플릿 엔진을 사용할 때 HTML 템플릿 파일들을 저장하는 디렉토리입니다. common, form, sample 등의 서브디렉토리로 구성될 수 있으며, 웹 페이지의 레이아웃이나 구성 요소를 정의합니다.

__pycache__: Python 인터프리터가 자동으로 생성하는 컴파일된 바이트코드 파일들을 저장하는 디렉토리입니다. 이 파일들은 Python 코드의 실행 속도를 향상시키기 위해 사용됩니다.

프로젝트 구조는 잘 구성되어 있으며, 각 구성 요소가 명확한 역할을 하고 있습니다. 이 구조를 기반으로 개발을 진행하면서 필요에 따라 추가적인 디렉토리나 파일을 생성하거나 조정할 수 있습니다.
```

