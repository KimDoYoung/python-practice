
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# chart_history.py
from sqlalchemy import DateTime,  Column, Integer, String, Text,  func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ChartHistory(Base):
    __tablename__ = 'chart_history'
    id = Column(Integer, primary_key=True, comment="자동증가")
    user_id = Column(String(50), nullable=False, default='ELIANA', comment="사용자id")
    chart_type = Column(String(20), nullable=False, comment="chart 종류")
    json = Column(Text, nullable=False, comment="입력 json")
    url = Column(String(200), nullable=False, comment="생성된 url")
    created_on = Column(DateTime, nullable=False, default=func.now(), comment="생성일시")

    def __init__(self, user_id, chart_type, json, url):
        self.user_id = user_id
        self.chart_type = chart_type
        self.json = json
        self.url = url

    def __repr__(self):
        return f"User ID: {self.user_id}, Chart Type: {self.chart_type}, JSON: {self.json}, URL: {self.url}, Created On: {self.created_on}"



def create_database():
    db_path = "sqlite:///eliana.db"
    engine = create_engine(db_path, echo=True)
    Base.metadata.create_all(engine)
    return engine

def add_chart_history(engine, chart_history):
    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(chart_history)
    session.commit()

    # 세션 닫기
    session.close()

# def add_chart_history(user_id, chart_type, json_data, url):
#     # 데이터베이스 엔진 생성
#     engine = create_database()

#     # 세션 설정
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     # 새로운 차트 히스토리 객체 생성 및 데이터베이스에 추가
#     new_chart = ChartHistory(user_id=user_id, chart_type=chart_type, json=json_data, url=url)
#     session.add(new_chart)
#     session.commit()

#     # 세션 닫기
#     session.close()