# estkrs

## 개요

- 공시정보-[공시검색](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001)에서 리스트를 검색한다.
  - url : <https://opendart.fss.or.kr/api/list.json>
  - method : GET
  - 날짜범위를 오늘을 기준으로  3개월
  - 상세구분 공시상세유형: C001
  - 여러페이지가 있을 수 있음에 유의

- 공시검색에서 조회한 회사리스트에서 DART고유번호를 취득해서 지분증권을 하나씩 조회한 후 결과를 ifi21에 채운다.
- ifi21에는 
- example 공시리스트

  ```text
  https://opendart.fss.or.kr/api/list.json?crtfc_key=apikey&bgn_de=20240912&end_de=20241112&pblntf_detail_ty=C001&page_no=1&page_count=100&sort=date&sort_mth=desc
  ```

- [증권신고서-지분증권](https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020054)을  가져와서 ifi21을 채운다
  - url: <https://opendart.fss.or.kr/api/estkRs.json>
         crtfc_key=api_key&
         corp_code=00968607&
         bgn_de=20240101&
         end_de=20241231>
