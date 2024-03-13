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
```
## 데이터베이스

* sqlite 를 사용 : eliana.db 

### 실행

```
uvicorn --app-dir src main:app --reload --port 8989
uvicorn main:app --reload --port 8989
```

### 폴더구조
```
project/
│
├── assets/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── images/
│       └── logo.png
│
├── templates/
│   └── index.html
│
└── main.py
```

 ### 테스트
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