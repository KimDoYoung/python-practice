# 파이썬 연습 프로젝트

## diary_to_html.py

* diary테이블의 내용을 가져와서 html파일로 만든다. 
* 만들어질 파일명, 날짜 범위를 가진다.
* .env에 db접속 정보를 넣어둔다.

### prompt
1. mysql 데이터베이스에 접속
2. "select * from diary" sql 수행
3. sql의 결과를 html 파일로 write

## package 
pip install mysql-connector-python
pip install python-dotenv

## .env
```
D_HOST="jskn.iptime.org"
D_DATABASE="kalpadb"
D_USER="kdy987"
D_PASSWORD="xxxx123!"
D_PORT=3306
```

## 사용법
1. 직접실행
```
python ./diary_to_html.py 202203.html 20220301 20220331

```
2. run_diary_to_html.sh


> 참고로 
>    1. diary은 ymd,summary,content 3개의 필드로 되어 있음.
>    2. 모든 필드 즉 3개의 필드는 모두 varchar타입임