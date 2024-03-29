
// 차트 유형에 따른 검증 함수 매핑
var validationFunctions = {
    'bar': validation_bar_chart_data,
    'line': validation_line_chart_data,
    'pie': validation_pie_chart_data
};
function validation_common(json_data) {
        var errors = [];
        // user_id 필수 검증
        if (typeof json_data.user_id !== 'string' || json_data.user_id.trim() === '') {
            errors.push("user_id는 필수이며, 비어있지 않은 문자열이어야 합니다.");
        }
        
        // result_type 필수 검증 및 값 확인
        if (!['url', 'stream'].includes(json_data.result_type)) {
            errors.push("result_type은 필수이며, 'url' 또는 'stream' 중 하나이어야 합니다.");
        }
        
        var chart_types = Object.keys(validationFunctions);

        // chart_type 검증
        if (!chart_types.includes(json_data.chart_type)) {
            errors.push("chart_type은 " + chart_types.join(",") + " 중 하나여야 합니다.");
        }
        
        // width, height 검증
        if (typeof json_data.width !== 'number' || json_data.width <= 0) {
            errors.push("width는 양의 정수여야 합니다.");
        }
        if (typeof json_data.height !== 'number' || json_data.height <= 0) {
            errors.push("height는 양의 정수여야 합니다.");
        }
        return errors;
    }
function validation_line_chart_data(json_data) {
    var errors = [];
    
    errors.push(...validation_common(json_data));
    
    // x_data 검증
    if (!Array.isArray(json_data.x_data) || !json_data.x_data.every(x => typeof x === 'number')) {
        errors.push("x_data는 숫자 배열이어야 합니다.");
    }
    
    // y_data 검증
    if (!Array.isArray(json_data.y_data) || !json_data.y_data.every(y => Array.isArray(y) && y.every(val => typeof val === 'number'))) {
        errors.push("y_data는 숫자 배열의 배열이어야 합니다.");
    }
    
    // line_colors 검증
    if (json_data.line_colors && (!Array.isArray(json_data.line_colors) || !json_data.line_colors.every(color => typeof color === 'string'))) {
        errors.push("line_colors는 문자열 배열이어야 합니다.");
    }
    
    // line_styles 검증
    if (json_data.line_styles && (!Array.isArray(json_data.line_styles) || !json_data.line_styles.every(style => typeof style === 'string'))) {
        errors.push("line_styles는 문자열 배열이어야 합니다.");
    }
    
    // line_widths 검증
    if (json_data.line_widths && (!Array.isArray(json_data.line_widths) || !json_data.line_widths.every(width => typeof width === 'number'))) {
        errors.push("line_widths는 숫자 배열이어야 합니다.");
    }
    
    // legend_labels 검증
    if (json_data.legend_labels && (!Array.isArray(json_data.legend_labels) || !json_data.legend_labels.every(label => typeof label === 'string'))) {
        errors.push("legend_labels는 문자열 배열이어야 합니다.");
    }
    
    // axis_range 검증
    if (json_data.axis_range && (!Array.isArray(json_data.axis_range) || json_data.axis_range.length !== 2 || !json_data.axis_range.every(range => Array.isArray(range) && range.length === 2 && range.every(val => typeof val === 'number')))) {
        errors.push("axis_range는 두 개의 [float, float] 튜플 배열이어야 합니다.");
    }
    
    // marker_styles 검증
    if (json_data.marker_styles && (!Array.isArray(json_data.marker_styles) || !json_data.marker_styles.every(style => typeof style === 'string'))) {
        errors.push("marker_styles는 문자열 배열이어야 합니다.");
    }
    
    // grid 검증
    if (typeof json_data.grid !== 'boolean') {
        errors.push("grid는 불리언이어야 합니다.");
    }
    
    // text_labels 검증
    if (json_data.text_labels && (!Array.isArray(json_data.text_labels) || !json_data.text_labels.every(labelGroup => Array.isArray(labelGroup) && labelGroup.every(label => Array.isArray(label) && label.length === 3 && typeof label[0] === 'number' && typeof label[1] === 'number' && typeof label[2] === 'string')))) {
        errors.push("text_labels는 [[float, float, string]] 형식의 배열이어야 합니다.");
    }

    // x_data의 길이와 y_data의 각 항목의 배열 길이 비교
    var xDataLength = json_data.x_data.length;
    var yDataLengthMismatch = json_data.y_data.some(y => y.length !== xDataLength);
    if (yDataLengthMismatch) {
        errors.push("x_data의 길이와 y_data의 각 항목의 배열 길이가 일치해야 합니다.");
    }
    return errors;
}
function validation_bar_chart_data(json_data) {
    var errors = [];

    errors.push(...validation_common(json_data));
    
    ['title', 'x_label', 'y_label'].forEach(label => {
        if (json_data[label] && typeof json_data[label] !== 'string') {
            errors.push(`${label}은(는) 문자열이어야 합니다.`);
        }
    });
    if (!Array.isArray(json_data.x_data) || !json_data.x_data.every(x => typeof x === 'number')) {
        errors.push("x_data는 숫자 배열이어야 합니다.");
    }
    if (!Array.isArray(json_data.y_data) || !json_data.y_data.every(y => Array.isArray(y) && y.every(val => typeof val === 'number'))) {
        errors.push("y_data는 숫자 배열의 배열이어야 합니다.");
    }
    if (json_data.bar_colors && (!Array.isArray(json_data.bar_colors) || json_data.bar_colors.length !== json_data.y_data.length)) {
        errors.push("bar_colors는 y_data와 길이가 같은 배열이어야 합니다.");
    }
    if (json_data.bar_widths && (!Array.isArray(json_data.bar_widths) || json_data.bar_widths.length !== json_data.y_data.length)) {
        errors.push("bar_widths는 y_data와 길이가 같은 배열이어야 합니다.");
    }
    if (json_data.legend_labels && (!Array.isArray(json_data.legend_labels) || json_data.legend_labels.length !== json_data.y_data.length)) {
        errors.push("legend_labels는 y_data와 길이가 같은 배열이어야 합니다.");
    }
    if (json_data.axis_range && (!Array.isArray(json_data.axis_range) || json_data.axis_range.length !== 2 || !json_data.axis_range.every(range => Array.isArray(range) && range.length === 2 && range.every(val => typeof val === 'number')))) {
        errors.push("axis_range는 두 개의 [float, float] 튜플 배열이어야 합니다.");
    }
    if (typeof json_data.grid !== 'boolean') {
        errors.push("grid는 불리언이어야 합니다.");
    }

    return errors;
}

function validation_pie_chart_data(json) {
    var errors = [];

    // 필수 필드 검증
    if (!json.labels || !Array.isArray(json.labels) || json.labels.length === 0) {
        errors.push("labels must be a non-empty array.");
    }
    if (!json.sizes || !Array.isArray(json.sizes) || json.sizes.length === 0) {
        errors.push("sizes must be a non-empty array.");
    }
    if (json.labels && json.sizes && json.labels.length !== json.sizes.length) {
        errors.push("labels and sizes arrays must have the same length.");
    }

    // 선택 필드 검증
    if (json.colors && (!Array.isArray(json.colors) || json.colors.length !== json.labels.length)) {
        errors.push("colors must be an array with the same length as labels.");
    }
    if (json.explode && (!Array.isArray(json.explode) || json.explode.length !== json.labels.length)) {
        errors.push("explode must be an array with the same length as labels.");
    }
    if (json.shadow !== undefined && typeof json.shadow !== "boolean") {
        errors.push("shadow must be a boolean.");
    }
    if (json.startangle !== undefined && typeof json.startangle !== "number") {
        errors.push("startangle must be a number.");
    }
    if (json.autopct !== undefined && typeof json.autopct !== "string") {
        errors.push("autopct must be a string.");
    }
    if (json.pctdistance !== undefined && typeof json.pctdistance !== "number") {
        errors.push("pctdistance must be a number.");
    }
    if (json.labeldistance !== undefined && typeof json.labeldistance !== "number") {
        errors.push("labeldistance must be a number.");
    }
    if (json.wedgeprops !== undefined && typeof json.wedgeprops !== "object") {
        errors.push("wedgeprops must be an object.");
    }
    if (json.textprops !== undefined && typeof json.textprops !== "object") {
        errors.push("textprops must be an object.");
    }
    if (json.radius !== undefined && typeof json.radius !== "number") {
        errors.push("radius must be a number.");
    }
    if (json.counterclock !== undefined && typeof json.counterclock !== "boolean") {
        errors.push("counterclock must be a boolean.");
    }
    if (json.frame !== undefined && typeof json.frame !== "boolean") {
        errors.push("frame must be a boolean.");
    }

    return errors;
}
