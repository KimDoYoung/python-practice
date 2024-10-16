from sqlalchemy import Column, String, BigInteger,  DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sys01Company(Base):
    __tablename__ = 'sys01_company'
    
    sys01_company_id = Column(BigInteger, primary_key=True)  # 회사ID (기본키)
    sys01_company_nm = Column(String(400), nullable=False)  # 회사명
    sys01_biz_no = Column(String(20), unique=True, nullable=False)  # 사업자등록번호 (고유 제약 조건)
    sys01_office_tel_no = Column(String(20))  # 전화번호1
    sys01_emgrcy_passwd = Column(String(20))  # 전화번호2
    sys01_office_fax_no = Column(String(20))  # 팩스번호1
    sys01_zip_cd = Column(String(10))  # 우편번호
    sys01_zip_addr = Column(String(400))  # 주소
    sys01_zip_detail = Column(String(400))  # 상세주소
    sys01_loc_nm = Column(String(40))  # 지역명
    sys01_anniv_date = Column(DateTime)  # 기념일
    sys01_note = Column(String(1000))  # 비고
    sys01_mail_info = Column(String(20))  # 메일서버정보
    sys01_mobile_tel_no = Column(String(20))  # 비상전화
    sys01_email_addr = Column(String(20))  # 비상이메일
    sys01_start_date = Column(DateTime)  # 설립일
    sys01_close_date = Column(DateTime)  # 계약종료일
    sys01_use_yn = Column(String(10))  # 사용여부
    sys01_emp_info = Column(String(400))  # 담당자(이름/부서/직책)
    sys01_cont_type = Column(String(100))  # X (특정 목적 미정)
    sys01_main_image_id = Column(BigInteger)  # X (특정 목적 미정)
    sys01_cycle_time = Column(String(10), default='60')  # X (특정 목적 미정, 기본값 60)
    sys01_leave_yn = Column(String(10))  # 휴가초과허용여부
    sys01_leave_month_cd = Column(String(2))  # 휴가결산월 (MonthsCode)
    sys01_leave_form_cd = Column(String(2))  # 휴가신청서 양식코드 (LeaveFormCode)
    sys01_icam_company_cd = Column(String(8))  # ICAM운용사코드
    sys01_ast_manager_auto_yn = Column(String(5))  # 자산담당자 자동생성 여부
    sys01_appr_step_lock_yn = Column(String(5))  # 결재선 잠금여부 (기본값 true)
    sys01_account_close_month = Column(String(2))  # 회계결산월 (MonthsCode)
    sys01_leave_compulsion_rt = Column(BigInteger)  # 휴가의무사용율 (%)
    sys01_ics_check_cycle_type = Column(String(1))  # 내부통제 체크리스트 주기 (M: 월, Q: 분기)
    sys01_tax_type = Column(String(1))  # 과세구분 (1: 면세, 2: 과세, 3: 공통)
    sys01_company_rep_nm = Column(String(20))  # 대외문서 (대표이사)
    sys01_mail_log_yn = Column(String(5))  # 메일기록여부
    sys01_ics_comply_cycle_type = Column(String(1))  # 내부통제 준수점검 주기 (M: 월, Q: 분기)
    sys01_dcr_numbering_cd = Column(String(1))  # 문서번호채번방식코드 (1: 연도별, 2: 연도-부서별)
    sys01_dcr_detail_use_yn = Column(String(5))  # 문서세부분류 사용여부
    sys01_apr_manager_info_yn = Column(String(5))  # 대외문서 담당자정보포함여부
    sys01_notice_date = Column(DateTime)  # 공지시작일
    sys01_owner_capital_apply_cd = Column(String(2))  # 자기자본적용일코드 (10: 최근, 20: 전전월말)
    sys01_ics_guide_yn = Column(String(5))  # 내부통제 문서연결 가이드 사용여부


