# gather-all

## 기능
다음과 같은 프로그램을 만들고 싶어요.
기능은 대상폴더의 모든 파일을 읽어서 1개의 파일로 만드는 것임.

조건은 다음과 같음
1. 프로그램명은 gatherall
2. 실행시 인자로 config을 입력받음 예를 들어 gatherall a.config 와 같이 실행함.
3. 인자가 없으면 usage 메세지를 보여주고 종료
4. config 파일 a.config는 다음과 같은 구조로 되어 있음

```
# 대상폴더
target-folder=c:\tmp
# 대상 파일들 *는 모든 문자열을 의미
target-files=*.java;*.css;*.html;web.xml
# exclude 할 파일들
exclude-files=assemble.obj; *.class
# 생성될 파일
c:/kdy/source1.dat
```
