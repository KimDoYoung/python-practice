import os
import fnmatch

def is_excluded(file_path, exclude_patterns, exclude_dirs):
    # 파일 패턴으로 배제
    for pattern in exclude_patterns:
        if fnmatch.fnmatch(file_path, pattern):
            return True
    # 디렉토리 경로로 배제
    for dir_path in exclude_dirs:
        if dir_path in file_path:
            return True
    return False

def gather_files(target_folder, exclude_files):
    exclude_patterns = [pattern for pattern in exclude_files if not pattern.endswith('/')]
    exclude_dirs = [pattern.rstrip('/') for pattern in exclude_files if pattern.endswith('/')]
    
    for root, dirs, files in os.walk(target_folder):
        for file in files:
            file_path = os.path.join(root, file)
            if not is_excluded(file_path, exclude_patterns, exclude_dirs):
                # 이 파일은 배제되지 않음
                print(file_path)  # 실제 구현에서는 여기서 파일 내용을 병합하거나 다른 처리를 할 수 있습니다.

# 예제 사용
target_folder = 'c:/tmp'
exclude_files = ['war/', 'test.java']
gather_files(target_folder, exclude_files)
