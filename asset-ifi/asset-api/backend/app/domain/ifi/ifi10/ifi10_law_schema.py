from pydantic import BaseModel
from typing import Optional
from decimal import Decimal

class Ifi10Law_Response(BaseModel):
    ifi10_law_id: Decimal  # 법규정보ID(PK)
    ifi10_law_cd: Optional[str]  # 법규코드(ics01_class_tree_cd)
    ifi10_law_nm: Optional[str]  # 법규명
    ifi10_relevant_law: Optional[str]  # 근거법규
    ifi10_submission: Optional[str]  # 제출처(공시방법)
    ifi10_cycle_type: Optional[str]  # 정기/수시구분(10:정기, 20:수시)
    ifi10_term_type: Optional[str]  # 기간/날짜구분(10:기간, 20:날짜)
    ifi10_interval_unit: Optional[str]  # 주기구분(D:일, W:주, M:월, Q:분기, H:반기, Y:년, O:수시)
    ifi10_std_date_type: Optional[str]  # 기준일타입(10:말일, 20:트리거(이벤트))
    ifi10_relative_position: Optional[str]  # 이전/이후구분(A:이전(이내), B:이후)
    ifi10_next_yn: Optional[str]  # 익월/익일여부(Y/N)
    ifi10_last_day_yn: Optional[str]  # 말일여부(Y/N)
    ifi10_value_month: Optional[Decimal]  # 값_월
    ifi10_value_week: Optional[Decimal]  # 값_주
    ifi10_value_weekday: Optional[Decimal]  # 값_요일
    ifi10_value_day: Optional[Decimal]  # 값_일
    ifi10_biz_calc_yn: Optional[str]  # 영업일계산여부(Y/N)
    ifi10_due_date_type: Optional[str]  # 기한일처리(10:해당없음, 20:직후영업일, 30:직전영업일)
    ifi10_start_date: Optional[str]  # 적용시작일(YYYYMMDD)
    ifi10_end_date: Optional[str]  # 적용종료일(YYYYMMDD)
    ifi10_deadline_nm: Optional[str]  # 기한정보
    ifi10_ics_class_tree_id: Optional[Decimal]  # 법규ID(ics01_class_tree_id)
    ifi10_deadline_id: Optional[Decimal]  # 기한ID(sch03_deadline_id)

    class Config:
        #orm_mode = True  # 반드시 orm_mode 활성화
        from_attributes = True  # from_orm 사용을 위한 설정 추가
