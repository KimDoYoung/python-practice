# 코드 샘플

## billboard chart

[api문서](https://naver.github.io/billboard.js/release/latest/doc/)
[데모](https://naver.github.io/billboard.js/demo/)

- create_billboard_chart를 호출 billboard_candle_chart.js

```javascript
<div id="candlestickChart_1"></div>
//columns
let column = []
let columns1 = ['data1'];
 for (let i = chart_data.length - 1; i >= 0; i--) {
        let item = chart_data[i];
        //시가, 고가, 저가, 종가
        columns1.push([
            Number(item.stck_oprc), 
            Number(item.stck_hgpr), 
            Number(item.stck_lwpr), 
            Number(item.stck_clpr)]
        );
}

column.push(column1);
create_billboard_candle_chart("offcanvas_daily_chart",columns, x_name)
```

## 종목명 offcanvas

```html
    회사정보
    <td>{{toggleCompanyCanvas stck_shrn_iscd hts_kor_isnm}}</td>
    상세보기로 이동
    <a href="/page?path=mystock/stock_detail&stk_code={{this.stk_code}}" class="btn btn-primary btn-sm" title="상세보기" target="_blank"><i class="bi bi-eye"></i></a>
```

## 관심추가

```html
<button class="btnAddAttension btn btn-warning btn-sm" data-stk-code="{{this.stk_code}}" data-stk-name="{{this.stk_name}}" title="관심..추가"><i class="bi bi-plus"></i></button>

```

```javascript
    $('#result-area').on("click", ".btnAddAttension", function() {
        //관심을 추가한다.
        const stk_code = $(this).data('stk-code');
        const stk_name = $(this).data('stk-name');
        const url = `/api/v1/mystock/add/stktype/${stk_code}/관심`;
        const data = {};
        putFetch(url, data).then(data => {
            console.log(data);
            alert(`${stk_name}(${stk_code}) 관심종목으로 추가되었습니다.`);
        }).catch(error=> {
            console.error(error.message);
        });
    });

```

## header sorting

```html
<a href="#" data-field="stck_prpr" class="sort-title">현재가<i class="bi"></i></a>

```

```javascript
let currentSort = { field: null, direction: 'asc' };

function makeTable() {
    let list = current_list
    if (list.length === 0) {
        $('#result-area').html('데이터가 없습니다.');
        return;
    }
    //필터
    if (filter_mbcr_name !== '') {
        list = list.filter(item => item.mbcr_name === filter_mbcr_name);
    }
    if(filter_dprt !== '') {
        list = list.filter(item => Number(item.dprt) <= Number(filter_dprt));
    }
    //정렬
    let fieldName = currentSort.field;
    if(fieldName){
        list.sort(function(a, b) {
            let x = parseFloat(a[fieldName]);
            let y = parseFloat(b[fieldName]);

            if (x < y) return currentSort.direction === 'asc' ? -1 : 1;
            if (x > y) return currentSort.direction === 'asc' ? 1 : -1;
            return 0;
        });
    }


    //템플릿으로 데이터 생성.
    const source = $('#investOpbysecItem-template').html();
    const template = Handlebars.compile(source);
    const html = template({list});
    $('#result-area').html(html);

    // 아이콘 설정
    const $resultArea = $('#result-area').find('table thead tr');
    $resultArea.find('.sort-title i').removeClass('bi-arrow-up bi-arrow-down');  // 모든 아이콘 제거
    var currentIcon = currentSort.direction === 'asc' ? 'bi-arrow-up' : 'bi-arrow-down';
    $resultArea.find('a[data-field="' + currentSort.field + '"] i').addClass(currentIcon);
    
}

    $('#result-area').on('click', '.sort-title', function() {
        const fieldName = $(this).data('field');
        console.log('sort:', fieldName);
        var isAscending = currentSort.field === fieldName && currentSort.direction === 'asc';
        currentSort.direction = isAscending ? 'desc' : 'asc';
        currentSort.field = fieldName;
        makeTable();
    });
```
