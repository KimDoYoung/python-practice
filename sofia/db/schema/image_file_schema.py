from sqlalchemy import  Column, Integer,  REAL, ForeignKey, Text
from sqlalchemy.orm import relationship

from db.schema.base_schema import BaseSchema



class ImageFileSchema(BaseSchema):
    __tablename__ = 'image_files'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    org_name = Column(Text, nullable=False)
    seq = Column(Integer, nullable=False)
    folder_id = Column(Integer, ForeignKey('image_folders.id'), nullable=True)
    image_format = Column(Text, nullable=True)
    image_width = Column(Integer, nullable=True)
    image_height = Column(Integer, nullable=True)
    image_mode = Column(Text, nullable=True)
    color_palette = Column(Text)
    camera_manufacturer = Column(Text)
    camera_model = Column(Text)
    capture_date_time = Column(Text)
    shutter_speed = Column(REAL)
    aperture_value = Column(REAL)
    iso_speed = Column(Integer)
    focal_length = Column(REAL)
    gps_latitude = Column(REAL)
    gps_longitude = Column(REAL)
    image_orientation = Column(Text)
    
    # 'image_folders' 테이블과의 관계 정의
    folder = relationship("ImageFolder", back_populates="image_files")

    def __repr__(self):
        return f"<ImageFile(org_name={self.org_name}, hash_code={self.hash_code}, seq={self.seq})>"