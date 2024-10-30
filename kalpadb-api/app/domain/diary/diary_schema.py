from typing import List, Optional
from pydantic import BaseModel, Field

class DiaryBase(BaseModel):
    ymd: str = Field(..., min_length=8, max_length=8)  # 날짜 형식 (yyyymmdd)
    content: str | None = None  # 내용 (선택적 필드)
    summary: Optional[str] = Field(None, max_length=300)  # 요약 (선택적 필드)

class DiaryUpdateRequest(BaseModel):
    content: str | None = None  # 내용 (선택적 필드)
    summary: Optional[str] = Field(None, max_length=300)  # 요약 (선택적 필드)


# 요청에 사용할 Pydantic 모델 (일기 작성 또는 수정용)
class DiaryRequest(BaseModel):
    ymd: str = Field(..., min_length=8, max_length=8)  # 날짜 형식 (yyyymmdd)
    content: str | None = None  # 내용 (선택적 필드)
    summary: Optional[str] = Field(None, max_length=300)  # 요약 (선택적 필드)
    attachments: Optional[list[str]] = None  # 첨부파일 배열 (선택적 필드)
# 응답에 사용할 Pydantic 모델
class DiaryResponse(BaseModel):
    ymd: str  # 일자
    content: str | None = None  # 내용
    summary: str | None = None  # 요약
    attachments : Optional[list[str]] = None # 첨부된 images url

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

class Attachment(BaseModel):
    node_id: str
    org_file_name: str
    file_size : int
    url : str
    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }
class DiaryDetailResponse(BaseModel):
    ymd: str  # 일자
    content: str | None = None  # 내용
    summary: str | None = None  # 요약
    attachments : Optional[list[Attachment]] = None # 첨부된 images url

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

class DiaryListResponse(BaseModel):
    ymd: str  # 일자
    content: str | None = None  # 내용
    summary: str | None = None  # 요약
    attachments : Optional[list[str]] = None # 첨부된 images url

    model_config = {
        'from_attributes': True  # ORM 모드 활성화
    }

# 페이징 처리를 위한 응답에 사용할 Pydantic 모델
class DiaryPageModel(BaseModel):
    data: List[DiaryResponse]  # 적절한 데이터 타입으로 대체하세요 (예: List[dict])
    data_count : int
    next_data_exists: bool
    last_index: int
    limit: int
    start_ymd: Optional[str]  # 날짜 형식에 따라 Optional[str] 사용
    end_ymd: Optional[str]
    order: Optional[str]