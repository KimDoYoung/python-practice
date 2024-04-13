from datetime import datetime
import shutil
import tempfile
import zipfile
from PIL import Image
from PIL.Image import Resampling  
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
from core.logger import get_logger

logger = get_logger(__name__)

def human_file_size(filesize: int) -> str:
    """파일 크기를 읽기 쉬운 형태로 변환하는 함수"""
    # 파일 크기 단위 정의
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB']:
        if filesize < 1024.0:
            return f"{filesize:.1f}{unit}"
        filesize /= 1024.0
    return f"{filesize:.1f}YB"

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

def create_pdf_from_images(image_paths, output_filename):
    """
    여러 이미지 파일들을 하나의 PDF 파일로 만듭니다.
    :param image_paths: 이미지 파일 경로 리스트
    :param output_filename: 출력될 PDF 파일 이름 (확장자 '.pdf' 포함)
    """
    # PDF 생성을 위한 캔버스 설정
    c = canvas.Canvas(output_filename, pagesize=letter)
    width, height = letter  # reportlab의 letter는 8.5*11 인치

    for path in image_paths:
        try:
            with Image.open(path) as img:
                if not os.path.exists(path):
                    continue
                img_width, img_height = img.size
                aspect_ratio = img_width / img_height

                # 이미지가 페이지 너비 또는 높이보다 크면 조정
                if img_width > width or img_height > height:
                    if (width / height) > aspect_ratio:
                        img_height = height
                        img_width = img_height * aspect_ratio
                    else:
                        img_width = width
                        img_height = img_width / aspect_ratio

                img = img.resize((int(img_width), int(img_height)), Resampling.LANCZOS)

                # tempfile을 사용하여 임시 파일 생성
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
                    img.save(tmp.name)

                    # 이미지를 페이지 하단에 배치
                    c.drawImage(tmp.name, 0, height - img_height, width=img_width, height=img_height)
                    c.showPage()
                    # 파일 경로를 저장
                    tmp_file_path = tmp.name

            # 처리가 끝난 임시 파일 삭제
            os.remove(tmp_file_path)
        except Exception as e:
            print(f"Failed to add {path}: {e}")

    # PDF 파일 저장
    c.save()

# 사용 예시
#image_paths = ['path/to/image1.jpg', 'path/to/image2.jpg', 'path/to/image3.jpg']
#output_zip_file = 'output_images.zip'
#create_zip_from_images(image_paths, output_zip_file)
def create_zip_from_images(image_paths, output_zip_filename):
    """
    여러 이미지 파일들을 하나의 ZIP 파일로 만듭니다.
    :param image_paths: 이미지 파일 경로 리스트
    :param output_zip_filename: 출력될 ZIP 파일의 전체 경로와 이름 (.zip 확장자 포함)
    """
    # ZIP 파일 생성
    with zipfile.ZipFile(output_zip_filename, 'w') as myzip:
        for image_path in image_paths:
            # ZIP 파일에 이미지 파일 추가
            myzip.write(image_path, arcname=os.path.basename(image_path))

def backup_and_rotate_image(original_path):
    """
    원본 이미지를 같은 폴더에 타임스탬프를 붙인 백업 파일로 복사하고, 복사된 이미지를 90도 회전하여 저장합니다.
    
    :param original_path: 원본 이미지 파일 경로
    """
    # 원본 파일명과 경로 추출
    folder_path, filename = os.path.split(original_path)
    file_root, file_ext = os.path.splitext(filename)

    # 타임스탬프 생성
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 백업 파일 경로 생성
    backup_filename = f"{file_root}_{timestamp}{file_ext}"
    backup_path = os.path.join(folder_path, backup_filename)

    # 원본 파일을 백업 경로로 복사
    shutil.copy2(original_path, backup_path)
    logger.debug(f"Backup created at {backup_path}")

    # 백업된 파일을 열어서 처리
    with Image.open(original_path) as img:
        # 이미지를 90도 오른쪽으로 회전 (시계 방향)
        rotated_img = img.rotate(-90, expand=True)
        # 회전된 이미지 저장
        rotated_img.save(original_path)
        logger.debug(f"Rotated image saved at {original_path}")