from datetime import datetime
import hashlib
from PIL import Image
from konlpy.tag import Okt

def todayYmd() -> str:
    ''' 오늘 날짜를 YYYYMMDD 형식으로 반환 '''
    return datetime.now().strftime("%Y%m%d")

def saved_path_to_url(files_str) -> list[str]:
    ''' 
    files_str: 파일 경로 문자열 (쉼표로 구분)
    파일 경로를 URL로 변환 (배열로 반환)
    /home/kdy987/www/uploaded/202401/IMG_20240117_080910.jpg
    '''
    base_url = "http://jskn.iptime.org:6789/uploaded/"
    if not files_str:
        return None
    # 파일 경로를 쉼표로 나눈 후, /home/kdy987/www/ 부분을 제거하고 URL로 변환
    files = files_str.split(",")
    # 빈 문자열을 제거하고 경로를 변환하여 리스트에 추가
    return [base_url + file.strip().replace("/home/kdy987/www/uploaded/", "") 
            for file in files if file.strip()]

def get_image_dimensions(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height

def get_file_hash(image_path):
    hash_algo = hashlib.sha256()
    with open(image_path, 'rb') as f:
        while chunk := f.read(8192):
            hash_algo.update(chunk)
    return hash_algo.hexdigest()

def extract_nouns(text: str) -> list:
    """
    한국어 텍스트에서 명사를 추출하는 함수.
    
    Args:
        text (str): 분석할 한국어 텍스트 (예: 일기 내용)
        
    Returns:
        list: 추출된 명사의 리스트
    """
    okt = Okt()
    lines = text.split("\n")  # 줄바꿈 기준으로 나누기
    nouns = []
    for line in lines:
        line = line.strip()
        nouns.extend(okt.nouns(line))  # 각 줄에서 명사 추출
    return nouns    
