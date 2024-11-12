# krx_std_code

## 개요

- ifi21를 대상으로 krx발행기관을 조회해서 발행기관코드등을 ifi20에 채운다.

- 로직
  1. ifi21의 최근날짜의 데이터로 [조회(https://isin.krx.co.kr/corp/corpList.do?method=corpInfoList)]해서 대상으로 한다.
  2. corp_nm으로 search_name stack을 구성, stack에는 원래 이름, 한글발음이름을 넣는다.
  3. stack을 돌면서 이름을 input 에 넣고 조회
  4. 나오는 리스트가 있으면
  5. 클릭해서 팝업창에서 약어가 원래 이름과 같으면 그 팝업창의 데이터를 수집 ifi20을 채운다.
