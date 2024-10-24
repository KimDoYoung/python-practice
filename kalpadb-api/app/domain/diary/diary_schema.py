from typing import Optional
from pydantic import BaseModel, Field

# 요청에 사용할 Pydantic 모델 (일기 작성 또는 수정용)
class DiaryRequest(BaseModel):
    ymd: str = Field(..., min_length=8, max_length=8)  # 날짜 형식 (yyyymmdd)
    content: str | None = None  # 내용 (선택적 필드)
    summary: Optional[str] = Field(None, max_length=300)  # 요약 (선택적 필드)
    attachments: Optional[list[str]] = None  # 첨부파일 배열 (선택적 필드)
# 응답에 사용할 Pydantic 모델
class DiaryListResponse(BaseModel):
    ymd: str  # 일자
    content: str | None = None  # 내용
    summary: str | None = None  # 요약
    attachments : Optional[list[str]] = None # 첨부된 images url

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

