from pydantic import BaseModel


class TextRequest(BaseModel):
    text: str

class SolarLunarResponse(BaseModel):
    solYmd: str
    lunYmd: str