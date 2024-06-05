from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class FieldMapping(BaseModel):
    Element: str
    한글명: str
    Type: str
    Required: str
    Length: int
    Description: str

KEY_MAPPING: List[FieldMapping] = [
    FieldMapping(Element="asst_icdc_erng_rt", 한글명="자산증감수익율", Type="String", Required="Y", Length=31, Description="데이터 미제공"),
    FieldMapping(Element="bfdy_sll_qty", 한글명="전일매도수량", Type="String", Required="Y", Length=10, Description="전일매도수량"),
    FieldMapping(Element="bfdy_buy_qty", 한글명="전일매수수량", Type="String", Required="Y", Length=10, Description="전일매수수량"),
    FieldMapping(Element="thdt_buyqty", 한글명="금일매수수량", Type="String", Required="Y", Length=10, Description="금일매수수량"),
    FieldMapping(Element="thdt_sll_qty", 한글명="금일매도수량", Type="String", Required="Y", Length=10, Description="금일매도수량"),
    # 추가 필드들...
]

# 한글명을 요소로 실제 필드를 찾는 함수
def get_element_by_korean_name(korean_name: str) -> Optional[str]:
    for field in KEY_MAPPING:
        if field.한글명 == korean_name:
            return field.Element
    return None
