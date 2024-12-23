# kind_scrap

## 개요

공시정보를 사이트 [KIND](https://kind.krx.co.kr/)에서 scrapping 해서 sqlite3 (파일DB)에 저장한다.
또한 가져온 데이터를 실행프로그램이 있는 폴더 하위에 tmp와 data에 저장된다.
tmp에는 목록데이터와 log파일이 저장되고 data에는 kind에서 관리하는 cd번호를 파일명으로 하는 내용이 저장된다.

## 사용법

python kind_scrap.py <start day yyyy-mm-dd> <end day yyyy-mm-dd> all|page_index

```shell
python kind_scrap.py 2024-12-13 2024-12-13 1 
python kind_scrap.py 2024-12-15 2024-12-23 all 
```

## 생성파일들

- scrapping결과는 data폴더하위에 각각의 cd로 생성됨
- scrap되는 데이터는 kindscrp_<start day>_<end day>.sqlite3 파일에 sqlite3 database로  저장됨
- tmp에 각 페이지의 공시 목록이 저장됨
