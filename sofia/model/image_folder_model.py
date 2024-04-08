from fastapi import Request
from model.base_model import BaseModel

class ImageFolderModel(BaseModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.folder_id = None
        self.folder_name = None
        self.last_load_time = None
        self.note = None
        self.image_files = []

