import sys
import os
import glob
import fnmatch


def read_config(config_path):
    # 설정 파일을 읽고 파싱하는 함수
    config = {}
    with open(config_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('#') or line.strip() == '':
                continue
            key, value = line.strip().split('=', 1)
            config[key.strip()] = value.strip()
    return config


#
#  만약 file_path가 dir이고 exclude_dirs에 포함되면  True
# 
def is_exclude_file(file_path, exclude_patterns):
    # 파일 이름 추출
    file_name = os.path.basename(file_path)
    
    # exclude_patterns 리스트를 순회하며 패턴 매칭 확인
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(file_name, pattern):
            return True  # 패턴에 일치하는 경우 True 반환
    return False  # 모든 패턴에 대해 일치하지 않는 경우 False 반환

def is_include_file(file_path, patterns):
    # 파일 이름 추출
    file_name = os.path.basename(file_path)
    
    # 주어진 패턴들과 파일 이름이 일치하는지 확인
    for pattern in patterns:
        if fnmatch.fnmatch(file_name, pattern):
            return True  # 패턴 중 하나라도 일치하면 True 반환
    return False  # 모든 패턴에 대해 일치하지 않으면 False 반환

def is_text_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            # 파일의 첫 1024바이트를 읽어서 확인
            data = file.read(1024)
            # 텍스트 파일로 간주할 수 있는 문자와 제어 문자를 제외한 것들
            text_chars = bytearray({7,8,9,10,12,13,27} | set(range(0x20, 0x100)) - {0x7f})
            return bool(data) and not bool(data.translate(None, text_chars))
    except IOError:
        return False  # 파일을 열 수 없는 경우

def gather_files(method, target_folder, target_patterns, exclude_files, output_file):
    print(f"target_folder : {target_folder}")
    exclude_patterns = [pattern for pattern in exclude_files if not pattern.endswith('/')]
    exclude_dirs = [pattern.rstrip('/') for pattern in exclude_files if pattern.endswith('/')]
    
    files_to_merge = [] # 골라서 합칠 파일들 목록
    for root, dirs, files in os.walk(target_folder):
        # 디렉토리 배제
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            if is_exclude_file(file_path, exclude_patterns):
                continue
            if is_include_file(file_path, target_patterns):
                files_to_merge.append(file_path)

    for selectedFile in files_to_merge:
        print(f"file: {selectedFile}")

    if method == 'list':
        return
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file in files_to_merge:
            if not is_text_file(file):
                continue
            print(f"파일 {file} 읽는 중...")
            with open(file, 'r', encoding='utf-8') as infile:
                outfile.write("-" * 80 + "\n")
                outfile.write(file+"\n");
                outfile.write("-" * 80 + "\n")
                outfile.write(infile.read() + "\n\n") # 파일 구분을 위해 두 줄 띄움

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gatherall <config_file>")
        print("gather all source files and merge those to one file")
        sys.exit(1)
    
    config_file = sys.argv[1]
    config = read_config(config_file)
    
    method = config.get('method')
    target_folder = config.get('target-folder')
    target_patterns = config.get('target-files').split(';')
    exclude_files = config.get('exclude-files').split(';')
    output_file = config.get('output-file')

    # target_folder validation
    if not os.path.exists(target_folder) or not os.path.isdir(target_folder):
        print(f"대상폴더 : {target_folder} 가 존재하지 않거나 폴더가 아닙니다")
        sys.exit(1)

    # 만들어질 파일이 존재하면 삭제함    
    if os.path.exists(output_file):
        os.remove(output_file)

    
    gather_files(method, target_folder, target_patterns, exclude_files, output_file)
    if method == 'merge':
        print(f"{output_file} created")
