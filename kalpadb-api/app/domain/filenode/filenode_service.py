from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.filenode.filenode_model import ApNode, ApFile, MatchFileVar

class ApNodeFileService:
    def __init__(self, db: AsyncSession):
        self.db = db

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
    async def get_file_by_match(self, tbl: str, id: str):
        stmt = (
            select(ApFile)
            .join(MatchFileVar, ApFile.node_id == MatchFileVar.node_id)
            .where(MatchFileVar.tbl == tbl)
            .where(MatchFileVar.id == id)
        )
        result = await self.db.execute(stmt)
        return result.scalars().all()
