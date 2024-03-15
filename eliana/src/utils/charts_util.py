from matplotlib import pyplot as plt
from constants import CHART_BASE_URL
from utils.file_utils import get_file_path


def create_bar_chart(request):
            
    # 파일 경로 생성
    file_path = get_file_path(request.width, request.height)

    # 차트 생성 로직 (matplotlib 사용)
    plt.figure(figsize=(request.width / 100, request.height / 100))

    if request.title:
        plt.title(request.title)
    if request.x_label:
        plt.xlabel(request.x_label)
    if request.y_label:
        plt.ylabel(request.y_label)
    if request.grid:
        plt.grid(request.grid)

    # 바 차트 그리기
    for i, y_data in enumerate(request.y_data):
        plt.bar(request.x_data, y_data, 
                color=request.bar_colors[i] if request.bar_colors else None,
                width=request.bar_widths[i] if request.bar_widths else None,
                label=request.legend_labels[i] if request.legend_labels else None)

    # 축 범위 설정
    if request.axis_range:
        plt.xlim(request.axis_range[0])
        plt.ylim(request.axis_range[1])

    # 범례 추가
    if request.legend_labels:
        plt.legend()

    plt.savefig(file_path)
    plt.close()

    # 생성된 이미지 파일의 URL 반환
    return f"{CHART_BASE_URL}/{file_path}"

def create_line_chart(request):
    # 파일 경로 얻기
    file_path = get_file_path(request.width, request.height)

    # 차트 생성 로직 (예: matplotlib 사용)
    plt.figure(figsize=(request.width / 100, request.height / 100))

    if request.title:
        plt.title(request.title)
    if request.x_label:
        plt.xlabel(request.x_label)
    if request.y_label:
        plt.ylabel(request.y_label)
    if request.grid:
        plt.grid(request.grid)

    # 라인 그리기
    for i, y_data in enumerate(request.y_data):
        plt.plot(request.x_data, y_data,
                color=request.line_colors[i] if request.line_colors else None,
                linestyle=request.line_styles[i] if request.line_styles else None,
                linewidth=request.line_widths[i] if request.line_widths else None,
                marker=request.marker_styles[i] if request.marker_styles else None,
                label=request.legend_labels[i] if request.legend_labels else None)

        # 텍스트 라벨 추가
        if request.text_labels:
            for text_label in request.text_labels[i]:
                plt.text(text_label[0], text_label[1], text_label[2])

    # 축 범위 설정
    if request.axis_range:
        plt.xlim(request.axis_range[0])
        plt.ylim(request.axis_range[1])

    # 범례 추가
    if request.legend_labels:
        plt.legend()

    plt.savefig(file_path)
    plt.close()

    # 생성된 이미지 파일의 URL 반환
    url = f"http://localhost:8989/{file_path}"
    return url