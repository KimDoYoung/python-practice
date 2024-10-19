from sqlalchemy import Column, String, DateTime, CHAR
from sqlalchemy.sql import func
from app.core.database import Base  # Base는 SQLAlchemy 모델의 부모 클래스

class ApNode(Base):
    __tablename__ = 'ap_node'

    id = Column(String(40), primary_key=True, comment='id')
    node_type = Column(CHAR(1), nullable=False, comment='노드종류 F: file, D: Directory')
    parent_id = Column(String(40), nullable=True, comment='부모노드id')
    name = Column(String(500), nullable=True, comment='노드명')
    full_name = Column(String(500), nullable=True, unique=True, comment='전체이름')
    owner_id = Column(String(20), nullable=False, comment='소유자ID')
    group_auth = Column(CHAR(3), nullable=False, comment='그룹권한: RWX')
    guest_auth = Column(CHAR(3), nullable=False, comment='guest권한')
    delete_yn = Column(CHAR(1), nullable=False, default='N', comment='삭제여부')
    create_dt = Column(DateTime, default=func.now(), comment='생성일시')
    modify_dt = Column(DateTime, nullable=True, comment='수정일시')
    upload_id = Column(String(20), nullable=True, comment='업로드 사용자id')

from sqlalchemy import Column, String, DateTime, DECIMAL, Integer
from sqlalchemy.sql import func
from app.core.database import Base

class ApFile(Base):
    __tablename__ = 'ap_file'

    node_id = Column(String(40), primary_key=True, comment='NODE ID')
    parent_node_id = Column(String(40), nullable=False, comment='부모노드 id')
    saved_dir_name = Column(String(500), nullable=False, comment='저장폴더')
    saved_file_name = Column(String(45), nullable=False, comment='저장파일명')
    org_file_name = Column(String(500), nullable=False, comment='원본파일명')
    file_size = Column(DECIMAL(10, 0), nullable=False, comment='파일크기')
    content_type = Column(String(100), nullable=True, comment='콘텐츠 타입')
    hashcode = Column(String(256), nullable=True, comment='해시코드')
    note = Column(String(300), nullable=True, comment='파일 설명')
    width = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    upload_dt = Column(DateTime, default=func.now(), comment='업로드일시')


class MatchFileVar(Base):
    __tablename__ = 'match_file_var'

    tbl = Column(String(20), primary_key=True, comment='매칭 테이블')
    id = Column(String(10), primary_key=True, comment='테이블 ID')
    node_id = Column(String(40), primary_key=True, comment='ap_file node_id')


class MatchFileInt(Base):
    __tablename__ = 'match_file_int'

    tbl = Column(String(20), primary_key=True, comment='매칭 테이블')
    id = Column(Integer, primary_key=True, comment='테이블 ID')
    node_id = Column(String(40), primary_key=True, comment='integer id 에 대한 ap_file과의 매칭')

