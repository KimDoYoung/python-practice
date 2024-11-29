from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.domain.filenode.filenode_service import ApNodeFileService
from app.domain.jangbi.jangbi_model import Jangbi
from app.domain.jangbi.jangbi_schema import JangbiListParam, JangbiListResponse, JangbiRequest, JangbiResponse
from app.core.settings import config
from app.core.logger import get_logger

logger = get_logger(__name__)
class JangbiService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert_jangbi(self, jangbi_id: Optional[int], request: JangbiRequest) -> Jangbi:
        """
        데이터가 존재하면 업데이트, 존재하지 않으면 새로 삽입한다.
        
        :param jangbi_id: 업데이트할 대상 ID (없으면 새로 생성)
        :param request: JangbiRequest 데이터
        :return: 생성되거나 업데이트된 Jangbi 객체
        """
        if jangbi_id:
            # 기존 데이터 확인
            existing_jangbi = await self.get_jangbi_by_id(jangbi_id)
            if existing_jangbi:
                # 업데이트 수행
                existing_jangbi.ymd = request.ymd
                existing_jangbi.item = request.item
                existing_jangbi.location = request.location
                existing_jangbi.cost = request.cost
                existing_jangbi.spec = request.spec
                existing_jangbi.lvl = request.lvl

                await self.db.commit()
                await self.db.refresh(existing_jangbi)
                return existing_jangbi

        # 존재하지 않으면 새로 생성
        new_jangbi = Jangbi(
            ymd=request.ymd,
            item=request.item,
            location=request.location,
            cost=request.cost,
            spec=request.spec,
            lvl=request.lvl
        )
        self.db.add(new_jangbi)
        await self.db.commit()
        await self.db.refresh(new_jangbi)
        return new_jangbi


    async def get_jangbi_by_id(self, jangbi_id: int) -> JangbiResponse:
        query = select(Jangbi).where(Jangbi.id == jangbi_id)
        result = await self.db.execute(query)
        jangbi = result.scalar_one_or_none()
        if not jangbi:
            return None
        fileService = ApNodeFileService(self.db)
        file_list = await fileService.get_file_by_match_int('jangbi', jangbi.id)
        attachs = []
        if file_list:
            for imgfile in file_list:
                saved_dir_name = imgfile.saved_dir_name.replace('/home/kdy987/www/uploaded/','')
                url = f"{config.URL_BASE}/{saved_dir_name}/{imgfile.saved_file_name}"
                attachs.append({
                    "node_id": imgfile.node_id,
                    "file_name": imgfile.org_file_name,
                    "file_size": imgfile.file_size,
                    "url": url,
                    "width" : imgfile.width,
                    "height" : imgfile.height
                })
        found_diary = JangbiResponse.model_validate(jangbi)
        found_diary.attachments = attachs
        return found_diary

    async def delete_jangbi(self, jangbi_id: int) -> bool:
        jangbi = await self.get_jangbi_by_id(jangbi_id)
        if not jangbi:
            return False

        await self.db.delete(jangbi)
        await self.db.commit()
        return True

    async def jangbi_list(self, param: JangbiListParam) -> JangbiListResponse:
        ''' 리스트 구하기 '''
        query = select(Jangbi).where(
            and_(
                Jangbi.ymd.between(param.start_ymd, param.end_ymd),
                func.concat(Jangbi.item, Jangbi.spec).like(f'%{param.search_text}%') if param.search_text else True,
                Jangbi.lvl == param.lvl if param.lvl else True
            )
        ).order_by(
            Jangbi.ymd.desc() if param.order_direction == 'desc' else Jangbi.ymd.asc()
        ).limit(param.limit + 1).offset(param.start_idx)
        
        result = await self.db.execute(query)
        jangbi_list = result.scalars().all()
        
        # Check if there is next data
        next_data_exists = len(jangbi_list) > param.limit
        if next_data_exists:
            jangbi_list = jangbi_list[:-1]  # Remove the extra item used for checking next data
        
        response_list = [JangbiListResponse.model_validate(jangbi) for jangbi in jangbi_list]
        
        return JangbiListResponse(
            list=response_list,
            item_count=len(response_list),
            next_data_exists=next_data_exists,
            next_index=param.start_idx + len(response_list)
        )