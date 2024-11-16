# asset-bat

- python으로 작성되는 배치프로그램들 모음
- 각 폴더 안에 독립적인 api관련 프로그램들을 갖고 있음
- asset-api에서 scheduling 으로 호출되어 짐.
- 각 폴더의 run.sh을 갖고 있어서 command line에서 수행가능
- logs 폴더 하위에 각 프로그램명 하위폴더에 저장됨

## 폴더

1. common : 공통 모듈
2. log : 각 모듈명을 서브폴더로 갖고 있으며 각각의 로그파일을 갖고 있음.
3. dart_code : DART CORP CODE를 가져와서 ifi20을 채움
4. estkrs : 증권신고서-지분증권을 가져와서 ifi21을 채움

> 각 폴더 안에 있는 README.md 에 더 상세하게 설명되어짐
