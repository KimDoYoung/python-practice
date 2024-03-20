# Merian

## 개요

1. 수집한 키보드  정보를 관리
    1. 키보드 정보를 테이블 keyboard를 통해서 관리
    2. 키보드와 관련된 이미지 파일을 관리
2. 최대한 chatGPT가 소스를 생성하게 한다


## virtual 환경 설정
- make_merian_folders.sh : 폴더 구조를 생성하는 bash shell 프로그램
- python -m venv env
- source .env/Scripts/activate

## test data
```
INSERT INTO public.edi_user (id,pw,nm,email,created_by)values('user1','$2b$12$C/MeW1GIhMe/W1nK45g7u.B.MrPzg4xQQDWFXZdCXYCfIA1xkClP2','김도영','kdy987@gmail.com','system');
```

## 실행환경
```
    source .env
    uvicorn backedn.main:app --reload --port $PORT
```
## 디버깅

* launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "backend.main:app",
                "--reload",
                "--port",
                "8686"  // 원하는 포트 번호로 변경
            ],
            "jinja": true
        }
    ]
}
```