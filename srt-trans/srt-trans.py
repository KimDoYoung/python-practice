# srt-trans.py
"""
모듈 설명: 
    - 영어자막을 한글자막으로 변환
    - srt파일을 대상으로 함
    - 구글 번역 API를 사용하여 번역
주요 기능:
    -   기능을 넣으시오

작성자: 김도영
작성일: 2024-12-23
버전: 1.0
"""
import sys
from googletrans import Translator
import os

def parse_srt(file_path):
    """
    SRT 파일을 읽어 자막 블록을 파싱
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    subtitles = []
    blocks = content.strip().split("\n\n")
    for block in blocks:
        lines = block.split("\n")
        index = int(lines[0])
        time_code = lines[1]
        text = "\n".join(lines[2:])
        subtitles.append({"index": index, "time_code": time_code, "text": text})
    return subtitles


def translate_subtitles(subtitles, src="en", dest="ko"):
    """
    자막 블록 번역
    """
    translator = Translator()
    for subtitle in subtitles:
        translated_text = translator.translate(subtitle["text"], src=src, dest=dest).text
        subtitle["text"] = translated_text
    return subtitles


def save_srt(file_path, subtitles):
    """
    번역된 자막을 SRT 형식으로 저장
    """
    with open(file_path, "w", encoding="utf-8") as file:
        for subtitle in subtitles:
            file.write(f"{subtitle['index']}\n")
            file.write(f"{subtitle['time_code']}\n")
            file.write(f"{subtitle['text']}\n\n")


def main():
    # 명령줄 인수 처리
    if len(sys.argv) != 2:
        print("Usage: python translate_srt.py <input_file>")
        return

    input_file = sys.argv[1]  # 명령줄 인수에서 입력 파일 경로 받기

    # 입력 파일 존재 확인
    if not os.path.exists(input_file):
        print(f"Input file '{input_file}' not found!")
        return

    # 출력 파일 이름 생성 (입력 파일 이름 기반)
    base_name, ext = os.path.splitext(input_file)  # 파일명과 확장자 분리
    output_file = f"{base_name}_ko{ext}"  # 예: abc.srt -> abc_ko.srt

    print("Parsing SRT file...")
    subtitles = parse_srt(input_file)

    print("Translating subtitles...")
    translated_subtitles = translate_subtitles(subtitles)

    print("Saving translated SRT file...")
    save_srt(output_file, translated_subtitles)

    print(f"Translation complete! Translated file saved as '{output_file}'.")


if __name__ == "__main__":
    main()