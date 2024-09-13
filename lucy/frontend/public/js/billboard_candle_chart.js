var billboard_chart;
function create_billboard_candle_chart(divId, columns, name) {
    let x_name = name || 'data1';

    billboard_chart = bb.generate({
        data: {
            // columns: [ [ "data1", [1327, 1369, 1289, 1348],   [1348, 1371, 1314, 1320] ] ], 시가,고가,저가,종가
            columns: columns,
            type: "candlestick", // for ESM specify as: candlestick()
            colors: {
                data1: "red"
            },
            labels: true,
            names: {
                data1: x_name
            }
        },
        candlestick: {
            color: {
                down: "blue"
            },
            width: {
                ratio: 0.5
            }
        },
        axis: {
            x: {
                padding: {
                left: 1,
                right: 1
                }
            }
        },
        bindto: d3.select("#" + divId)
    });
}

function extract_candle_data(list, openField, highField, lowField, closeField) {
    let column1 = ['data1'];  // 초기 값 설정
    
    // 리스트의 각 항목을 순회하여 필드에 맞는 데이터를 추출
    for (let i = list.length - 1; i >= 0; i--) {
        let item = list[i];
        
        // 주어진 필드명을 사용해 시가, 고가, 저가, 종가 데이터를 배열로 추가
        column1.push([
            Number(item[openField]),  // 시가
            Number(item[highField]),  // 고가
            Number(item[lowField]),   // 저가
            Number(item[closeField])  // 종가
        ]);
    }

    return column1;  // 완성된 데이터를 반환
}
/**
const $td = $('<td></td>').append('<canvas width="200" height="50"></canvas>');
// canvas 요소 선택
const canvas = $td.find('canvas')[0];
const ctx = canvas.getContext('2d');
drawHorizontalCandle(ctx, data.open, data.close, data.high, data.low);
*/
// 옆으로 누운 캔들바를 그리는 함수
function drawHorizontalCandle(ctx, open, close, high, low) {
    const candleWidth = 20;  // 캔들 두께
    const height = ctx.canvas.height;

    const openX = Math.min(open, close); // 왼쪽 기준점 (open과 close 중 작은 값)
    const closeX = Math.max(open, close); // 오른쪽 기준점 (open과 close 중 큰 값)

    const highX = high;  // 캔들 윗꼬리 끝
    const lowX = low;    // 캔들 아래꼬리 끝

    // 배경 클리어
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    // 캔들 윗꼬리 (high)
    ctx.beginPath();
    ctx.moveTo(highX, height / 2);
    ctx.lineTo(closeX, height / 2);
    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
    ctx.stroke();

    // 캔들 몸통
    ctx.fillStyle = open > close ? "red" : "blue"; // 시가 > 종가면 붉은 캔들
    ctx.fillRect(openX, (height - candleWidth) / 2, closeX - openX, candleWidth);

    // 캔들 아래꼬리 (low)
    ctx.beginPath();
    ctx.moveTo(openX, height / 2);
    ctx.lineTo(lowX, height / 2);
    ctx.stroke();
}