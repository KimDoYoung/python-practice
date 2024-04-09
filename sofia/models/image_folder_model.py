from datetime import datetime
from typing import List, Optional
from sqlmodel import SQLModel, Field

from models.image_file_model import ImageFileBase

class ImageFoldersBase(SQLModel):
    folder_name: str
    last_load_time: Optional[datetime] = None
    note:  Optional[str] = None

class ImageFolders(ImageFoldersBase, table=True):
    __tablename__ = 'image_folders'
    id: Optional[int] = Field(default=None, primary_key=True)
    last_load_time: datetime = Field(sa_column_kwargs={"default": datetime.now, "nullable": False})

class ImageFoldersCreate(ImageFoldersBase):
    pass

class ImageFoldersUpdate(ImageFoldersBase):
    folder_name: Optional[str] = None
    last_load_time: Optional[datetime] = None
    note: Optional[str] = None

class ImageFolderWithFiles(ImageFoldersBase):
    files : Optional[List[ImageFileBase]] = None
