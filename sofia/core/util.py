
from datetime import datetime
from PIL import Image
import os


def datetime_serializer(obj):
    """datetime 객체를 직렬화하기 위한 함수"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def safe_float_conversion(value):
    """실수로 변환하는 함수, 실패시 None을 반환"""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def convert_to_datetime(date_str):
    """문자열을 datetime 객체로 변환하는 함수"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None  # 유효하지 않은 날짜 문자열일 경우 None을 반환

def is_image_file(filename):
    '''파일명으로 이미지 파일 여부를 판단하는 함수'''
    # 지원하는 이미지 파일 확장자 리스트
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    # 파일의 확장자를 추출하고 소문자로 변환하여 유효한지 확인
    extension = os.path.splitext(filename)[1].lower()
    return extension in valid_extensions

# MIME 타입을 결정하는 함수
def get_mime_type(file_name):
    """파일명으로 MIME 타입을 결정하는 함수"""
    extension = os.path.splitext(file_name)[1].lower()
    if extension == ".jpg" or extension == ".jpeg":
        return "image/jpeg"
    elif extension == ".png":
        return "image/png"
    elif extension == ".gif":
        return "image/gif"
    else:
        return "application/octet-stream"  # 기본값


# 사용 예
# image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg']  # 이미지 파일 경로 리스트
# output_path = 'output.pdf'  # 출력될 PDF 파일 경로
# images_to_pdf(image_paths, output_path)
def images_to_pdf(image_paths, output_path):
    """이미지 파일들(배열)을 PDF로 변환하는 함수"""
    # 이미지 파일들을 열고, PIL 이미지 객체의 리스트를 생성
    images = [Image.open(image_path) for image_path in image_paths]

    # 첫 번째 이미지를 기준으로 PDF 저장
    # 나머지 이미지들은 append_images 리스트에 추가
    images[0].save(output_path, save_all=True, append_images=images[1:])
