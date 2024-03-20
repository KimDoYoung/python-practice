from sqlalchemy import Column, Integer, String, BigInteger, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Keyboard(Base):
    __tablename__ = 'keyboard'
    __table_args__ = {'schema': 'collections'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(100))
    manufacturer = Column(String(100))
    purchase_date = Column(String(8))
    purchase_amount = Column(BigInteger)
    key_type = Column(String(10))
    switch_type = Column(String(20))
    actuation_force = Column(String(10))
    interface_type = Column(String(30))
    overall_rating = Column(Integer)
    typing_feeling = Column(Text)
    create_on = Column(DateTime, default=func.now())
    create_by = Column(String(30), nullable=True)
