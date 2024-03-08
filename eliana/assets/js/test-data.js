var testLineData = {
    "user_id" : "kdy987",
    "result_type": "url",
    "chart_type": "line",
    "width": 800,
    "height": 600,
    "title": "Line Chart 샘플",
    "x_data": [1.0, 2.0, 3.0, 4.0, 5.0],
    "y_data": [
        [2.0, 4.0, 6.0, 8.0, 10.0],
        [3.0, 6.0, 9.0, 12.0, 15.0]
    ],
    "x_label": "X-axis",
    "y_label": "Y-axis 온도축",
    "line_colors": ["blue", "red"],
    "line_styles": ["solid", "dashed"],
    "line_widths": [2.0, 1.5],
    "legend_labels": ["Data 1", "Data 2"],
    "axis_range": [[0.0, 6.0], [0.0, 16.0]],
    "marker_styles": ["o", "s"],
    "grid": true,
    "text_labels": [
        [
        [2.0, 4.0, "Point 2, 4"],
        [4.0, 8.0, "Point 4, 8"]
        ],
        [
        [2.0, 6.0, "Point 2, 6"],
        [4.0, 12.0, "Point 4, 12"],
        [5.0, 10.0, "확인!"]
        ]
    ]
};

var testBarData ={
    "user_id": "kdy987",
    "result_type": "url",
    "chart_type": "bar",
    "width": 800,
    "height": 600,
    "title": "Line Chart 샘플",
    "x_data": [1, 2, 3, 4, 5],
    "y_data": [[5, 7, 3, 8, 9], [2, 4, 6, 1, 3]],
    "x_label": "X 축 라벨",
    "y_label": "Y 축 라벨",
    "bar_colors": ["blue", "green"],
    "bar_widths": [0.4, 0.4],
    "legend_labels": ["데이터 시리즈 1", "데이터 시리즈 2"],
    "axis_range": [[0, 6], [0, 10]],
    "grid": true
}
;

var testData = {
    'line' : testLineData,
    'bar'  : testBarData
}