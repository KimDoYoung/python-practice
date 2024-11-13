import hashlib
import os

alphabet_to_korean = {
    "A": "에이", "B": "비", "C": "씨", "D": "디", "E": "이", "F": "에프", "G": "지",
    "H": "에이치", "I": "아이", "J": "제이", "K": "케이", "L": "엘", "M": "엠", "N": "엔",
    "O": "오", "P": "피", "Q": "큐", "R": "알", "S": "에스", "T": "티", "U": "유",
    "V": "브이", "W": "더블유", "X": "엑스", "Y": "와이", "Z": "제트"
}

def generate_korean_pronunciation_variants(org_corp_nm):
    ''' 회사명에 알파벳이 포함된 경우 한글 발음으로 변환하여 반환합니다. 리턴값: 배열(변환된 한글 발음, 원본 텍스트) '''
    result = []
    converted_text = []  # 변환된 한글 발음을 저장할 리스트
    contains_alphabet = False  # 알파벳이 포함되어 있는지 확인하는 플래그

    for char in org_corp_nm:
        if char.upper() in alphabet_to_korean:  # 알파벳인 경우 변환
            converted_text.append(alphabet_to_korean[char.upper()])
            contains_alphabet = True
        else:  # 알파벳이 아닌 경우 그대로 추가
            converted_text.append(char)

    # 변환된 텍스트와 원본 텍스트의 배열을 리턴
    if contains_alphabet:
        result.append(''.join(converted_text))  # 변환된 텍스트 추가
    result.append(org_corp_nm)  # 원본 텍스트 추가

    return result

def calculate_file_hash(file_path, hash_algo="sha256"):
    """주어진 파일의 해시 값을 계산하여 반환합니다."""
    hash_func = hashlib.new(hash_algo)
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def is_file_unchanged(file_path, hash_file="last_hash.txt"):
    """파일이 기존 파일과 동일한지 확인합니다."""
    # 파일의 현재 해시 값 계산
    current_hash = calculate_file_hash(file_path)
    
    # 이전 해시 값이 기록된 파일이 존재하는지 확인
    if os.path.exists(hash_file):
        with open(hash_file, "r") as f:
            last_hash = f.read().strip()
        # 현재 해시와 이전 해시 비교
        if current_hash == last_hash:
            print("파일이 변경되지 않았습니다.")
            return True
        else:
            print("파일이 변경되었습니다.")
    else:
        print("이전 해시 기록 파일이 없습니다.")

    # 새 해시 값 기록
    with open(hash_file, "w") as f:
        f.write(current_hash)
    
    return False