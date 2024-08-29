from typing import Literal, Optional
from beanie import Document

class StkInfo(Document):
    market: Optional[Literal["KSP", "KSD"]]=""
    stk_code: str
    stk_name: str
    exp_code: Optional[str]='' # LS 확장코드

    class Settings:
        collection = "StkInfo"