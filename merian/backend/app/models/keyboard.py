from sqlalchemy import CHAR, TIMESTAMP, Column, ForeignKey, Integer, String, BigInteger, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class KeyboardModel(Base):
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


class FBFile(Base):
    __tablename__ = 'fb_file'
    __table_args__ = {'schema': 'public'}

    file_id = Column(Integer, primary_key=True)
    node_id = Column(Integer, nullable=False)
    phy_folder = Column(String(300), nullable=False)
    phy_name = Column(String(300), nullable=False)
    org_name = Column(String(300), nullable=False)
    mime_type = Column(String(100))
    file_size = Column(Integer)
    ext = Column(String(50))
    note = Column(String(1000))
    width = Column(Integer)
    height = Column(Integer)
    status = Column(CHAR(1), default='N', nullable=False)
    create_on = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
    create_by = Column(String(30))

class FileCollectionMatch(Base):
    __tablename__ = 'file_collection_match'
    __table_args__ = {'schema': 'public'}

    category = Column(String(100), primary_key=True, default='keyboard')
    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('public.fb_file.file_id'), primary_key=True)
    file = relationship("FBFile")
