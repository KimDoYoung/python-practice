
from sqlalchemy.exc import IntegrityError
from sqlalchemy import UniqueConstraint, create_engine
from sqlalchemy.orm import sessionmaker
# chart_history.py
from sqlalchemy import DateTime,  Column, Integer, String, Text,  func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///eliana.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

Session = sessionmaker(autoflush=False, bind=engine)

class ChartHistory(Base):
    __tablename__ = 'chart_history'
    id = Column(Integer, primary_key=True, comment="자동증가")
    user_id = Column(String(50), nullable=False, default='ELIANA', comment="사용자id")
    chart_type = Column(String(20), nullable=False, comment="chart 종류")
    json = Column(Text, nullable=False, comment="입력 json")
    url = Column(String(200), nullable=False, comment="생성된 url")
    created_on = Column(DateTime, nullable=False, default=func.now(), comment="생성일시")
    __table_args__ = (UniqueConstraint('user_id', 'json', name='_user_id_json_uc'),)

    def __init__(self, user_id, chart_type, json, url):
        self.user_id = user_id
        self.chart_type = chart_type
        self.json = json
        self.url = url

    def __repr__(self):
        return f"User ID: {self.user_id}, Chart Type: {self.chart_type}, JSON: {self.json}, URL: {self.url}, Created On: {self.created_on}"


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close();

def add_chart_history(chart_history):
    session = Session()
    try:
        session.add(chart_history)
        session.commit()
    except IntegrityError:
        session.rollback()
        # 유니크 제약 조건 위반 처리 로직
        print("이미 존재하는 user_id와 JSON 조합입니다.")
    finally:
        session.close()

Base.metadata.create_all(engine)