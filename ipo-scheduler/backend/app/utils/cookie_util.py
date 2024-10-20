from fastapi import Response, Request
import json


def set_cookie(response: Response, key: str, value: dict):
    value_str = json.dumps(value)
    response.set_cookie(
        key=key, value=value_str,
        # domain="localhost",
        # path="/keyboard",
        # httponly=True,  # 클라이언트 사이드 스크립트 접근 방지
         max_age=3600,  # 1시간 후 쿠키 만료
         expires=1800,  # 30분 후 쿠키 만료
        # secure=False,  # HTTPS를 통해서만 쿠키 전송. 실제 배포에서 주석 해제
        # samesite='Lax'  # strict 쿠키를 동일한 사이트에서만 전송
    )


def get_cookie(request: Request, key: str, default: str = "{}"):  # 기본값을 "{}"로 설정
    value_str = request.cookies.get(key, default)
    if isinstance(value_str, str):  # 반환 값이 문자열인지 확인
        try:
            return json.loads(value_str)
        except json.JSONDecodeError:
            return json.loads(default)  # JSON 파싱 오류 시 기본값 반환
    return json.loads(default)  # 반환 값이 문자열이 아닌 경우 기본값 반환


def delete_cookie(response: Response, key: str):
    response.delete_cookie(key=key)