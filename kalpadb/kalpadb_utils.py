def generate_srch_key(file_name):
    """
    파일명을 받아 srch_key를 생성하는 함수
    :param file_name: 문자열로 된 파일명
    :return: 변환된 srch_key 문자열
    """
    srch_key = ""
    for char in file_name:
        if '가' <= char < '나':
            srch_key += '1'
        elif '나' <= char < '다':
            srch_key += '2'
        elif '다' <= char < '라':
            srch_key += '3'
        elif '라' <= char < '마':
            srch_key += '4'
        elif '마' <= char < '바':
            srch_key += '5'
        elif '바' <= char < '사':
            srch_key += '6'
        elif '사' <= char < '아':
            srch_key += '7'
        elif '아' <= char < '자':
            srch_key += '8'
        elif '자' <= char < '차':
            srch_key += '9'
        elif '차' <= char < '카':
            srch_key += '0'
        elif '카' <= char < '타':
            srch_key += '!'
        elif '타' <= char < '파':
            srch_key += '@'
        elif '파' <= char < '하':
            srch_key += '#'
        elif '하' <= char:
            srch_key += '$'
        elif char.isalnum():  # 알파벳 또는 숫자
            srch_key += char
        # 공백(space)은 무시
    return srch_key
