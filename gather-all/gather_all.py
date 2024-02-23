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

def filter_files(files, exclude_patterns):
    # 제외할 파일 필터링
    filtered_files = []
    for file in files:
        exclude = any(glob.fnmatch.fnmatch(file, pattern) for pattern in exclude_patterns)
        if not exclude:
            filtered_files.append(file)
    return filtered_files

def is_excluded(file_path, exclude_patterns, exclude_dirs):
    # 파일 패턴으로 배제
    for pattern in exclude_patterns:
        if file_path.startswith("."):
            return True
        if fnmatch.fnmatch(file_path, pattern):
            return True
    # 디렉토리 경로로 배제
    for dir_path in exclude_dirs:
        if dir_path.startswith("."):
            return True
        if dir_path in file_path:
            return True
    return False

def gather_files(target_folder, target_patterns, exclude_files, output_file):
    print(f"target_folder : {target_folder}")
    exclude_patterns = [pattern for pattern in exclude_files if not pattern.endswith('/')]
    exclude_dirs = [pattern.rstrip('/') for pattern in exclude_files if pattern.endswith('/')]
    
    files_to_merge = [] # 골라서 합칠 파일들 목록
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            print(f"file : {file_path}")
            if not is_excluded(file_path, exclude_patterns, exclude_dirs):
                files_to_merge.append(file_path)

    for selectedFile in files_to_merge:
        print(f"file: {selectedFile}")

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for file in files_to_merge:
            print(f"파일 {file} 읽는 중...")
            with open(file, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read() + "\n\n") # 파일 구분을 위해 두 줄 띄움

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gatherall <config_file>")
        print("gather all source files and merge those to one file")
        sys.exit(1)
    
    config_file = sys.argv[1]
    config = read_config(config_file)
    
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

    
    gather_files(target_folder, target_patterns, exclude_files, output_file)
