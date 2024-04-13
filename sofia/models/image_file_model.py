from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
import datetime

class ImageFileBase(SQLModel):
    org_name: str
    seq: int
    folder_id: Optional[int] = Field(default=None, foreign_key="image_folders.id")
    image_size: Optional[int] = None
    image_format: Optional[str] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    image_mode: Optional[str] = None
    color_palette: Optional[str] = None
    camera_manufacturer: Optional[str] = None
    camera_model: Optional[str] = None
    capture_date_time: Optional[datetime.datetime] = None  
    shutter_speed: Optional[float] = None
    aperture_value: Optional[float] = None
    iso_speed: Optional[int] = None
    focal_length: Optional[float] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    image_orientation: Optional[str] = None
    thumb_path: Optional[str] = None
    file_time : Optional[datetime.datetime] = None  # 파일 생성 시간

class ImageFile(ImageFileBase, table=True):
    __tablename__ = "image_files"    
    id: Optional[int] = Field(default=None, primary_key=True)

class ImageFileCreate(ImageFileBase):
    pass

class ImageFileUpdate(ImageFileBase):
    org_name: Optional[str] = None
    seq: Optional[int] = None
    folder_id: Optional[int] = None
    image_format: Optional[str] = None
    image_width: Optional[int] = None
    image_height: Optional[int] = None
    image_mode: Optional[str] = None
    color_palette: Optional[str] = None
    camera_manufacturer: Optional[str] = None
    camera_model: Optional[str] = None
    capture_date_time: Optional[datetime.datetime] = None
    shutter_speed: Optional[float] = None
    aperture_value: Optional[float] = None
    iso_speed: Optional[int] = None
    focal_length: Optional[float] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    image_orientation: Optional[str] = None

