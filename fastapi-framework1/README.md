# fastapi framework

## 개요

- url에 따라서 jinja로 HTMLResponse를 하는 프로젝트
- 프로젝트의 구성에 따른 폴더구성 및 각 파일들의 역활정의

> 프로젝트를 mvc style, full stack style, rest-api style 이렇게 3가지로 나누자
>
1. mvc style : 화면을 생성, 부분적으로 ajax를 통한 json제공
2. full stack : backend, frontend.로 폴더를 구분하면서 생성
3. rest-api : json만을 제공

## 특징

- 폴더명에 단수형
- main.py에서 설정
- core 에 config.py, logger.py, exceptions.py 등 생성
- 환경변수로 profile의 시작, 변수명 project_MODE

```shell
    export JOANNA_MODE=local
```
