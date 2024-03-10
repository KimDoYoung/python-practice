# chart_history.py
from sqlalchemy import DateTime, create_engine, Column, Integer, String, Text, Date, func
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
