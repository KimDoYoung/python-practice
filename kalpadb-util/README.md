# kalpadb - utils

## hdd

- 2T HDD의 파일정보를 hdd table에 넣는다.
- python hdd F 영화29
- 실행 : 윈도우에서 실행

```shell
python hdd.py f '영화1'
```

## ap_file_wh.py

1. 개요: maria database의 테이블 ap_file의 width, height column을 채운다.
2. sql "select * from ap_file where content_type like 'image%' and width is null;" 로 조회
3. saved_dir_name과 saved_file_name을 조합해서 물리적 파일명을 구한 후
4. 이미지 파일에서 width와 height를 구한다.
5. ap_file 테이블의 컬럼 width와 height를 update한다.
6. hash_code를 구해서 테이블 컬럼 hashcode를 채운다.
7. 실행 : jskn에서 docker-compose로 실행

```shell
cd kalpdb-util
docker-compose ps
docker-compose down
docker-compose up --build -d
```

## make_thumb.py

1. 개요: ap_file의 column thumb_path를 채운다.
2. 다음과 같은 sql을 수행

```sql
    select saved_dir_name, saved_file_name 
    from ap_file
    where thumb_path is null
    and content_type like 'image%'
```

3. thumb_base_dir은  /home/kdy/uploaded/thumbs이다
4. thumb_base_dir하위에 이미지파일의 생성일자중 yyyymm을 가지고 하위폴더를 만들어 그 폴더에 생성한다.
5. 이미지 width가 300px보다 크면 width를 300으로 맞추고, 이미지의 width x height 원래 비율에 맞게끔 height를 설정한다.
6. thumb 이미지는 모두 png형식으로 한다.
