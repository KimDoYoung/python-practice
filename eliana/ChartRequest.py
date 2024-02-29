# ChartRequest.py
from pydantic import BaseModel
from typing import List

class ChartRequest(BaseModel):
    type : str = 'url'
    width: int = 300
    height: int = 200
    x: List[str] = []
    y: List[float] = []
