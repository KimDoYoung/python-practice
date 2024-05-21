# scrapy-test

## 개요

- 2가지 툴을 연습
- web browser 자동화 (매크로 작성)
- selenium으로 웹페이지 테스트

## 3가지 tools

1. web scrpping의 tool들을 테스트

- Beautiful Soup: HTML과 XML 파일에서 데이터를 추출하기 위해 널리 사용되는 라이브러리입니다. 사용하기 쉽고 강력하여, 복잡한 HTML 구조에서도 데이터를 쉽게 추출할 수 있습니다.

- Scrapy: 아주 강력한 웹 크롤링 및 스크래핑 프레임워크로, 크롤링 규칙을 설정하여 대규모 웹사이트 데이터를 효율적으로 추출할 수 있습니다. 비동기 처리를 지원하며, 여러 페이지를 동시에 처리할 수 있어 속도 면에서 우수합니다.

- Selenium: 원래 웹 애플리케이션 테스트를 위해 개발된 도구지만, JavaScript를 통해 동적으로 생성된 데이터를 포함한 웹 페이지의 데이터를 추출할 때 유용합니다. 웹 브라우저를 실제로 제어하여 페이지 상호작용을 모방할 수 있습니다.

## 외국에서 제공하는 데이터

- [yahoo finance](https://finance.yahoo.com/quote/005930.KS/history)

## 파일 설명

- s38_2.py : 38커뮤니케이션에서 2 페이지를 가져와서 mongodb ipo_scrp collection에 넣음.
- f38_2.py : ipo_scrap -> ipo collection으로 필요한 데이터만 format바꿔서 넣음.

## 수식

- 간단한 수식 계산기가 필요할 듯 해서 만들어 달라고 하다

1. 수식을 계산하는 모듈을 만들고 싶음
2. 다음과 같은 수식(문자열)들을 db에 저장해 둠
   예1) (buyer_high + seller_high ) / 2  * bias
3. module명 lucy_calc.py
4. 다음과 같이 사용

    ```text

    varialbes  = {
        buyer_high = 10
        seller_high = 20
        bias = 0.2
    }
    template = (buyer_high + seller_high ) / 2  * bias
    value = calc(template, varialbes)
    print(value)
    ```

5. calc.py를 만들어 줘
