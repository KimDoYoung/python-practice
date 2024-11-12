# dart_code

## 개요

1. [DART OpenAPI](https://opendart.fss.or.kr/intro/main.do)를 사용하여 가져온 데이터를 ifi20에 넣음
2. URL: <https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=api_key>
   다운로드되는 파일 corpCode.xml은 크롬과 edge에서는 실제로 zip파일임
3. corp_code로 찾아서 있으면 update, 없으면 insert한다
4. id는 SELECT f_create_batchseq() 로 채번함

## 실행

1. asset-api에서 스케줄링에 의해서 호출됨
2. command line에서 run.sh에 의해 실행될 수 있음
3. logs/dart_code/에 로그파일이 생김
