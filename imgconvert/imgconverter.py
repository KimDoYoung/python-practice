import os
import argparse
from PIL import Image

def convert_images(target_folder, src_format, dest_format):
    # 대상 폴더의 파일을 순회
    for filename in os.listdir(target_folder):
        # 파일의 전체 경로 생성
        file_path = os.path.join(target_folder, filename)

        # 파일이 이미지 확장자와 일치하면 변환 수행
        if filename.lower().endswith('.' + src_format.lower()):
            # 이미지를 열고 변환
            with Image.open(file_path) as img:
                # 변환할 파일의 새 경로 및 이름
                new_filename = filename[:-len(src_format)] + dest_format
                new_file_path = os.path.join(target_folder, new_filename)

                # 이미지 저장
                img.save(new_file_path)
                print(f"Converted {filename} to {new_filename}")

def main():
    parser = argparse.ArgumentParser(description="Convert images from one format to another within a specified folder.")
    parser.add_argument("target_folder", type=str, help="The folder containing images to convert.")
    parser.add_argument("src_format", type=str, help="Source image format (e.g., jpg, png)")
    parser.add_argument("dest_format", type=str, help="Destination image format (e.g., png, jpg)")
    
    try:
        args = parser.parse_args()
        convert_images(args.target_folder, args.src_format, args.dest_format)
    except SystemExit:
        # argparse가 자동으로 출력하는 도움말 이후에 추가 정보를 제공
        print(f"\nExample: python {os.path.basename(__file__)} ./images jpg png\n")

if __name__ == "__main__":
    main()
