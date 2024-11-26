# kalpadb - utils

## hdd

- 2T HDD의 파일정보를 hdd table에 넣는다.
- python hdd F 영화29

## ap_file_wh.py

1. 개요: maria database의 테이블 ap_file의 width, height column을 채운다.
2. sql "select * from ap_file where content_type like 'image%' and width is null;" 로 조회
3. saved_dir_name과 saved_file_name을 조합해서 물리적 파일명을 구한 후
4. 이미지 파일에서 width와 height를 구한다.
5. ap_file 테이블의 컬럼 width와 height를 update한다.
