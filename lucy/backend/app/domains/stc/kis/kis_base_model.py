from pydantic import BaseModel
from typing import Any

from backend.app.domains.stc.kis.kis_mapping import KEY_MAPPING

class KisBaseModel(BaseModel):
    def get(self, key: str) -> Any:
        mapped_key = KEY_MAPPING.get(key, key)
        return getattr(self, mapped_key, None)
