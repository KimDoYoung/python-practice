var billboard_chart;
function create_billboard_chart(columns, name) {
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
        bindto: "#offcanvas_daily_chart"
    });
}


