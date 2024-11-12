from sqlalchemy import Column, Numeric, Date, Text, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import TIMESTAMP

Base = declarative_base()

class Ifi21ApiData(Base):
    __tablename__ = "ifi21_api_data"
    __table_args__ = {"schema": "public"}

    ifi21_api_data_id = Column(Numeric, primary_key=True, nullable=False, comment="API수집데이터ID(PK)")
    ifi21_config_api_id = Column(Numeric, nullable=True, comment="API관리ID(ifi91_config_api_id)")
    ifi21_date = Column(Date, nullable=True, comment="수집일자")
    ifi21_date_time = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("CURRENT_TIMESTAMP"), comment="수집일시")
    ifi21_request = Column(Text, nullable=True, comment="요청값")
    ifi21_success_yn = Column(String(5), nullable=True, comment="성공여부(true/false)")
    ifi21_status_cd = Column(String(10), nullable=True, comment="결과코드")
    ifi21_status_msg = Column(String(200), nullable=True, comment="결과메세지")
    ifi21_response = Column(Text, nullable=True, comment="결과값")
    ifi21_search1 = Column(String(50), nullable=True, comment="검색어1")
    ifi21_search2 = Column(String(50), nullable=True, comment="검색어2")

    def __repr__(self):
        return (f"<Ifi21ApiData(ifi21_api_data_id={self.ifi21_api_data_id}, "
                f"ifi21_config_api_id={self.ifi21_config_api_id}, ifi21_date={self.ifi21_date}, "
                f"ifi21_date_time={self.ifi21_date_time}, ifi21_request='{self.ifi21_request}', "
                f"ifi21_success_yn='{self.ifi21_success_yn}', ifi21_status_cd='{self.ifi21_status_cd}', "
                f"ifi21_status_msg='{self.ifi21_status_msg}', ifi21_response='{self.ifi21_response}', "
                f"ifi21_search1='{self.ifi21_search1}', ifi21_search2='{self.ifi21_search2}')>")