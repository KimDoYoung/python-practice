# kalpadb-api

- 기존에 있던 kalpadb(mysql) 에 대한 restful api
- frontend는 만들지 않는다.
- 짝으로 된 client는 svelte로 만들기로 한다.
- fastapi
- mysql async
- fastapi로 restful api 서버를 만들려고 함.
- mysql로 된 데이터베이스명 kalpadb가 존재함.
- localhost나 알려진 IP로 접속시에만 서비스를 제공함
- 기본포트를 8088로 함

## 실행

```shell
pip install -r requirements.txt
export KALPADB_API_MODE=local
uvicorn app.main:app --reload
```

## JSKN에 배포

1. kalpadb-api폴더로 이동
2. .env.real 확인
3. docker-compose up --build -d
4. docker ps kalpadb-api
5. docker logs kalpadb-api
6. 브라우저에서 http://...:8088/docs

## 특이점 (docker설치시 필요)

1. **한글형태소(KoNLPy)** 분석때문에 jdk1.8 이 설치되어 있어야 한다.
    - $JAVA_HOME 확인
2. **네이버에서 한자찾기** 때문에selenium이 설치되어 있어야 한다.

## Diary

- List

```sql
select 
 A.ymd
 ,A.summary
 ,A.content
 ,GROUP_CONCAT(concat(C.saved_dir_name,'/', C.saved_file_name) order by concat(C.saved_dir_name,'/', C.saved_file_name)   SEPARATOR ', ') as files
from dairy A 
left outer join match_file_var B
 on  A.ymd = B.id and B.tbl ='dairy'
left outer join ap_file C 
 on B.node_id  = C.node_id
where A.ymd between '20240101' and '20241231'
group by A.ymd, A.summary, A.content
order by A.ymd
```

## 영화진흥회(KOFIC) 에서 영화목록찾기

-제목으로 영화찾기

```text
https://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=xxx
&movieNm=%ED%86%A0%ED%83%88
&curPage=1
&itemPerPage=100
```

- 상세정보

```text
http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?
movieCd=2024A442
&key=xxx
```

-
