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