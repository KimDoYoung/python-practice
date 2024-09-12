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
        bindto: "#" + divId
    });
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
    ctx.fillStyle = open > close ? "red" : "green"; // 시가 > 종가면 붉은 캔들
    ctx.fillRect(openX, (height - candleWidth) / 2, closeX - openX, candleWidth);

    // 캔들 아래꼬리 (low)
    ctx.beginPath();
    ctx.moveTo(openX, height / 2);
    ctx.lineTo(lowX, height / 2);
    ctx.stroke();
}