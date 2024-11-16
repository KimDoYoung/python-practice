from sqlalchemy import Column, Numeric, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import VARCHAR
from sqlalchemy.sql import func

Base = declarative_base()

class IFI20DartCorp(Base):
    __tablename__ = 'ifi20_dart_corp'
    __table_args__ = {'schema': 'public'}
    
    ifi20_dart_corp_id = Column(Numeric, primary_key=True, nullable=False, comment='발행기관정보ID(PK)')
    ifi20_dart_corp_cd = Column(VARCHAR(8), nullable=True, comment='DART기관코드')
    ifi20_dart_corp_nm = Column(VARCHAR(100), nullable=True, comment='DART기관명')
    ifi20_stk_cd = Column(VARCHAR(12), nullable=True, comment='종목코드')
    ifi20_iss_corp_cd = Column(VARCHAR(5), nullable=True, comment='발행기관코드')
    ifi20_iss_corp_nm = Column(VARCHAR(100), nullable=True, comment='발행기관명')
    ifi20_iss_corp_snm = Column(VARCHAR(100), nullable=True, comment='발행기관약명')
    ifi20_iss_corp_enm = Column(VARCHAR(100), nullable=True, comment='발행기관영문명')
    ifi20_corp_reg_no = Column(VARCHAR(13), nullable=True, comment='법인등록번호(-제거)')
    ifi20_biz_reg_no = Column(VARCHAR(10), nullable=True, comment='사업자등록번호(-제거)')
    ifi20_addr = Column(VARCHAR(100), nullable=True, comment='주소')
    ifi20_eaddr = Column(VARCHAR(100), nullable=True, comment='영문주소')
    ifi20_ceo = Column(VARCHAR(50), nullable=True, comment='대표이사')
    ifi20_tel = Column(VARCHAR(50), nullable=True, comment='대표전화')
    ifi20_homepage = Column(VARCHAR(50), nullable=True, comment='홈페이지')
    ifi20_market_type = Column(VARCHAR(50), nullable=True, comment='시장구분')
    ifi20_list_yn = Column(VARCHAR(10), nullable=True, comment='상장여부')
    ifi20_industry_class = Column(VARCHAR(100), nullable=True, comment='업태')
    ifi20_industry_item = Column(VARCHAR(100), nullable=True, comment='업종')
    ifi20_work_date = Column(TIMESTAMP(timezone=True), server_default=func.current_timestamp(), nullable=True, comment='작업일시')

    def __repr__(self):
        return (f"<Ifi20DartCorp(ifi20_dart_corp_id={self.ifi20_dart_corp_id}, "
                f"ifi20_dart_corp_cd='{self.ifi20_dart_corp_cd}', ifi20_dart_corp_nm='{self.ifi20_dart_corp_nm}', "
                f"ifi20_stk_cd='{self.ifi20_stk_cd}', ifi20_iss_corp_cd='{self.ifi20_iss_corp_cd}', "
                f"ifi20_iss_corp_nm='{self.ifi20_iss_corp_nm}', ifi20_iss_corp_snm='{self.ifi20_iss_corp_snm}', "
                f"ifi20_iss_corp_enm='{self.ifi20_iss_corp_enm}', ifi20_corp_reg_no='{self.ifi20_corp_reg_no}', "
                f"ifi20_biz_reg_no='{self.ifi20_biz_reg_no}', ifi20_addr='{self.ifi20_addr}', "
                f"ifi20_eaddr='{self.ifi20_eaddr}', ifi20_ceo='{self.ifi20_ceo}', "
                f"ifi20_tel='{self.ifi20_tel}', ifi20_homepage='{self.ifi20_homepage}', "
                f"ifi20_market_type='{self.ifi20_market_type}', ifi20_list_yn='{self.ifi20_list_yn}', "
                f"ifi20_industry_class='{self.ifi20_industry_class}', ifi20_industry_item='{self.ifi20_industry_item}', "
                f"ifi20_work_date={self.ifi20_work_date})>")