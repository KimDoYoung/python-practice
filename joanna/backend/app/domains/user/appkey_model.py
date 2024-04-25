from sqlmodel import  Field
from typing import Optional
from datetime import datetime
from backend.app.domains.user.user_model import User
from backend.app.domains.base_sql_model import BaseSQLModel


class AppKeyBase(BaseSQLModel):
    user_id: str = Field(foreign_key="public.users.user_id", max_length=30, nullable=False)
    key_name: str = Field(primary_key=True, max_length=30)
    
class AppKey(AppKeyBase, table=True, schema="public"):
    __tablename__ = "appkeys"
    __table_args__ = {'schema': 'public'}
    key_value: str = Field(max_length=200, nullable=False)
    use_yn: str = Field(default='Y', max_length=1, nullable=False)
    issuer: Optional[str] = Field(default=None, max_length=100, nullable=True)
    note: Optional[str] = Field(default=None, max_length=500, nullable=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
