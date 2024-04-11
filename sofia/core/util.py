
from datetime import datetime
import os


def datetime_serializer(obj):
    """datetime 객체를 직렬화하기 위한 함수"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def is_image_file(filename):
    # 지원하는 이미지 파일 확장자 리스트
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    # 파일의 확장자를 추출하고 소문자로 변환하여 유효한지 확인
    extension = os.path.splitext(filename)[1].lower()
    return extension in valid_extensions

# MIME 타입을 결정하는 함수
def get_mime_type(file_name):
    extension = os.path.splitext(file_name)[1].lower()
    if extension == ".jpg" or extension == ".jpeg":
        return "image/jpeg"
    elif extension == ".png":
        return "image/png"
    elif extension == ".gif":
        return "image/gif"
    else:
        return "application/octet-stream"  # 기본값