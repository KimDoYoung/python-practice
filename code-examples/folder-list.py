import os

def filter_files(files, extension):
    return [file for file in files if file.endswith(extension)]

def list_folders_and_pdf_files(directory, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                folder_path = os.path.join(root, dir)
                print(folder_path, file=output_file)  # 수정됨
            pdf_files = filter_files(files, '.pdf')  # PDF 파일 필터링
            for pdf_file in pdf_files:
                file_path = os.path.join(root, pdf_file)
                print(file_path, file=output_file)  # 수정됨

# 출력 파일 경로
output_file_path = "list.txt"

# 디렉토리 경로 변경
directory_path = "f:/"
list_folders_and_pdf_files(directory_path, output_file_path)
