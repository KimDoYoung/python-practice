from datetime import datetime
from typing import List, Optional
from fastapi import Form
from sqlmodel import SQLModel, Field

from models.image_file_model import ImageFile, ImageFileBase

class ImageFolderBase(SQLModel):
    folder_name: str
    folder_path: str
    last_load_time: Optional[datetime] = None
    note:  Optional[str] = None

class ImageFolder(ImageFolderBase, table=True):
    __tablename__ = 'image_folders'
    id: Optional[int] = Field(default=None, primary_key=True)
    last_load_time: datetime = Field(sa_column_kwargs={"default": datetime.now, "nullable": False})

class ImageFolderCreate(ImageFolderBase):
    pass

class ImageFolderUpdate(ImageFolderBase):
    folder_name: Optional[str] = None
    last_load_time: Optional[datetime] = None
    note: Optional[str] = None

class ImageFolderWithFiles(ImageFolderBase):
    files : Optional[List[ImageFile]] = None

class FolderExport(SQLModel):
    folder_id: int
    export_type: str
    
    @classmethod
    def as_form(
        cls,
        folder_id: int = Form(...),
        export_type: str = Form(...)
    ) -> "FolderExport":
        return cls(folder_id=folder_id, export_type=export_type)
