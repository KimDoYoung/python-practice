# 파이썬 연습 프로젝트

## diary_to_html.py

### prompt
1. mysql 데이터베이스에 접속
2. "select * from diary" sql 수행
3. sql의 결과를 html 파일로 write

## package 
pip install mysql-connector-python

## 사용법

```
python ./diary_to_html.py 202203.html 20220301 20220331

```

> 참고로 
>    1. diary은 ymd,summary,content 3개의 필드로 되어 있음.
>    2. 모든 필드 즉 3개의 필드는 모두 varchar타입임