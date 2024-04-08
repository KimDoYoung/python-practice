from sqlalchemy import create_engine, Column, Integer, String, REAL, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from db.schema.base_schema import BaseSchema


class ImageFolderSchema(BaseSchema):
    __tablename__ = 'image_folders'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    folder_name = Column(Text, nullable=False)
    last_load_time = Column(Text, default="CURRENT_TIMESTAMP")
    note = Column(Text)
    
    # 'image_files' 테이블과의 관계 정의
    image_files = relationship("ImageFile", back_populates="folder")

    def __repr__(self):
        return f"<ImageFolder(folder_name={self.folder_name}, last_load_time={self.last_load_time})>"