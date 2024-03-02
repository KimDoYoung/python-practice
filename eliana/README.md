# Eliana

## 개요

1. chart server
   1. 사용자로부터 chart를 그리는 데이터를 받아서 그것으로 chart 이미지를 만들고 url 또는 stream을 리턴한다.
   
2. 기술스택
   * FastAPI
   * Matplotlib
   * PostgreSQL
   * JWT

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
```

### 실행

```
uvicorn main:app --reload --port 8989
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