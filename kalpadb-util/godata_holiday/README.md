# godata_holiday.py

## 개요

- godata에서 공휴일 정보를 가져와서 calendar table에 넣는다.
- 구분: H, 양력: S, ymd,  content를 채운다.
- 인자는 2개를 받는다. 년도와 월
- 인자를 1개 받으면 년도로 생각
- 인가가 생략되면 오늘의 년도와 월로 간주
- 입력받은 인자의 년,월로부터 12개월 미래로 가면서 공휴일 정보를 가져와서 caldendar에 채운다.
- 만약 이미 존재하면 insert하지 않는다.
