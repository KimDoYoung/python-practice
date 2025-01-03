import os
import uuid
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.filenode.filenode_model import ApNode, ApFile, MatchFileInt, MatchFileVar

class ApNodeFileService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    def getUuid(self):
        """UUID를 생성하고 대시(-)를 제거한 문자열을 반환합니다."""
        return uuid.uuid4().hex  # 대시를 제거하려면 .hex 사용

    async def rotate_image(self, file_id: int, degree: int) -> bool:
        ''' file_id에 해당하는 이미지 degree만큰 회전 '''
        ap_file = self.get_file_by_node_id(file_id)
        if ap_file is None:
            raise ValueError("해당 ID에 해당하는 파일이 없습니다.")
        image_path = os.path.join(ap_file.saved_dir_name, ap_file.saved_file_name)
        image = Image.open(image_path)
        clock_degree = -1 * degree
        rotated_image = image.rotate(clock_degree, expand=True)
        rotated_image.save(image_path)
        return True

    # 파일 및 노드 생성
    async def create_ap_node_and_file(self, ap_node_data, ap_file_data):
        new_node = ApNode(**ap_node_data.dict())
        new_file = ApFile(**ap_file_data.dict())
        self.db.add(new_node)
        self.db.add(new_file)
        await self.db.commit()
        await self.db.refresh(new_node)
        await self.db.refresh(new_file)
        return new_node, new_file

    # ap_node와 ap_file 조인 후 데이터 조회
    async def get_node_and_file(self, node_id: str):
        stmt = (
            select(ApNode, ApFile)
            .join(ApFile, ApNode.id == ApFile.node_id)
            .where(ApNode.id == node_id)
        )
        result = await self.db.execute(stmt)
        return result.first()

    # match_file_var로 매칭된 파일 조회
    async def get_file_by_match(self, tbl: str, id: str) -> list[ApFile]:
        ''' match_file_var에서 id 즉 일기 같은 경우 ymd 매칭된 파일들 모두 조회 '''
        stmt = (
            select(ApFile)
            .join(MatchFileVar, ApFile.node_id == MatchFileVar.node_id)
            .where(MatchFileVar.tbl == tbl)
            .where(MatchFileVar.id == id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
    
    # match_file_int로  매칭된 파일 조회
    async def get_file_by_match_int(self, tbl: str, id: int) -> list[ApFile]:
        ''' match_file_int id 즉 장비  '''
        stmt = (
            select(ApFile)
            .join(MatchFileInt, ApFile.node_id == MatchFileInt.node_id)
            .where(MatchFileInt.tbl == tbl)
            .where(MatchFileInt.id == id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()    


    async def get_file_in_match_by_id_and_node_id(self, tbl: str, id: str, node_id: str) -> ApFile:
        ''' match_file_var에서 id와 node_id로 1개 조회 '''
        stmt = (
            select(ApFile)
            .join(MatchFileVar, ApFile.node_id == MatchFileVar.node_id)
            .where(MatchFileVar.tbl == tbl)
            .where(MatchFileVar.id == id)
            .where(MatchFileVar.node_id == node_id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def get_file_by_node_id(self, node_id: str) -> ApFile:
        ''' node_id로 ap_file 1레코드  조회 '''
        stmt = select(ApFile).where(ApFile.node_id == node_id)
        result = await self.db.execute(stmt)
        return result.scalar()
    
    async def get_node_by_id(self, node_id: str) -> ApNode:
        ''' node_id로 ap_node  조회 '''
        stmt = select(ApNode).where(ApNode.id == node_id)
        result = await self.db.execute(stmt)
        return result.scalar()
    
    async def delete_note_by_id(self, node_id: str):
        ''' node_id로 ap_node 1레코드  삭제 '''
        stmt = select(ApNode).where(ApNode.id == node_id)
        result = await self.db.execute(stmt)
        node = result.scalar()
        self.db.delete(node)
        await self.db.commit()
        return node
    
    async def delete_file_by_id(self, node_id: str):
        ''' node_id로  ap_file record 1개 삭제 '''
        stmt = select(ApFile).where(ApFile.node_id == node_id)
        result = await self.db.execute(stmt)
        file = result.scalar()
        self.db.delete(file)
        await self.db.commit()
        return file
    
    async def set_note(self, node_id: str, note: str) -> ApFile:
        ''' ap_file의  note (comment) 수정 '''
        stmt = select(ApFile).where(ApFile.node_id == node_id)
        result = await self.db.execute(stmt)
        node = result.scalar()
        if node is None:
            return None
        node.note = note
        await self.db.commit()
        return node