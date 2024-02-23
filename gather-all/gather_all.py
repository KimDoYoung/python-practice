import sys
import os
import glob

def read_config(config_path):
    # 설정 파일을 읽고 파싱하는 함수
    config = {}
    with open(config_path, 'r') as f:
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

def gather_files(target_folder, target_patterns, exclude_files, output_file):
    # 파일 병합 작업 수행
    files_to_merge = []
    for pattern in target_patterns:
        files_to_merge.extend(glob.glob(os.path.join(target_folder, pattern)))

    files_to_merge = filter_files(files_to_merge, exclude_files)

    with open(output_file, 'w') as outfile:
        for file in files_to_merge:
            with open(file, 'r') as infile:
                outfile.write(infile.read() + "\n\n") # 파일 구분을 위해 두 줄 띄움

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gatherall <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    config = read_config(config_file)
    
    target_folder = config.get('target-folder')
    target_patterns = config.get('target-files').split(';')
    exclude_files = config.get('exclude-files').split(';')
    output_file = config.get('output-file')
    
    gather_files(target_folder, target_patterns, exclude_files, output_file)
