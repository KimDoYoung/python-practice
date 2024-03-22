import aiofiles
from fastapi import UploadFile


async def save_file(file: UploadFile, path: str) -> str:
    """
    파일을 비동기적으로 저장합니다.
    :param file: 저장할 파일 객체.
    :param path: 파일을 저장할 서버 상의 경로.
    :return: 저장된 파일의 경로.
    """
    async with aiofiles.open(path, 'wb') as out_file:
        # UploadFile.file은 starlette.datastructures.UploadFile에서 제공하는 비동기 파일 객체입니다.
        contents = await file.read()  # 파일 내용을 읽습니다.
        await out_file.write(contents)  # 읽은 내용을 파일에 씁니다.
    return path