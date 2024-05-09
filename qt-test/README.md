# qt 테스트

## 개요

- qt designer를 이용해서 qt gui 프로그램

## 명령어들

- python -m pip install --upgrade pip
- python -m pip install --upgrade setuptools

## 화면생성방법

```text
1. designer에서 편집
2. 저장 1.ui
3. /c/Users/deHong/Python312/Scripts/pyuic5
4. pyuic5 1.ui -o 1.py
```

## 참고

- [위키](https://wikidocs.net/21853)

## chatGPT로 Prompt1

qt5로 ui를 만들고 싶음. 요구 조건은 아래와 같음

1. 어플리케이션 아이콘은 a.png로함
2. 실행시 모니터의 중앙에 띄움
3. 풀다운메뉴를 갖음
   1. File -> 1.Config 2.  Quit 메뉴를 갖음
4. 바탕화면은 왼쪽판넬과 오른쪽 판넬로 나뉘어짐 두개는 splitter로 구분되어 조절가능해야함
5. 왼쪽에는 vertical로 버튼을 3개 넣음, 버튼의 라벨은 menu1, menu2, menu3임
6. 오른쪽은 탭으로 구성됨 탭은 3개로 구성되며 왼쪽의 menu버튼들과 연결됨
