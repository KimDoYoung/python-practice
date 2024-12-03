import os
import shutil
from typing import List
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy import Boolean, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.util import get_file_hash, get_image_dimensions, todayYmd
from app.domain.filenode.filenode_model import ApFile, ApNode, MatchFileInt
from app.domain.filenode.filenode_schema import AttachFileInfo
from app.domain.filenode.filenode_service import ApNodeFileService
from app.domain.jangbi.jangbi_model import Jangbi
from app.domain.jangbi.jangbi_schema import JangbiListParam, JangbiListResponse, JangbiResponse, JangbiUpsertRequest
from app.core.settings import config
from app.core.logger import get_logger

logger = get_logger(__name__)
class JangbiService:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def get_1(self, jangbi_id: int) -> Jangbi:
        query = select(Jangbi).where(Jangbi.id == jangbi_id)
        result = await self.db.execute(query)
        jangbi = result.scalar_one_or_none()
        return jangbi
    
    async def get_jangbi_parent_node_id(self) -> str:
        ''' 장비 부모 노드 ID 조회 '''
        parent_node_query = select(ApNode.id).where(
            (ApNode.node_type == 'D') & 
            (ApNode.name == '장비')
        ).limit(1)

        parent_node_result = await self.db.execute(parent_node_query)
        parent_node_id = parent_node_result.scalar_one_or_none() 
        return parent_node_id    

    async def upsert_jangbi(self, request: JangbiUpsertRequest) -> JangbiResponse:
        """
        데이터가 존재하면 업데이트, 존재하지 않으면 새로 삽입한다.
        
        :param jangbi_id: 업데이트할 대상 ID (없으면 새로 생성)
        :param request: JangbiRequest 데이터
        :return: 생성되거나 업데이트된 Jangbi 객체
        """
        jangbi_id = request.id
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
        new_jangbi_response = JangbiResponse.model_validate(new_jangbi)
        return new_jangbi_response


    async def get_jangbi_by_id(self, jangbi_id: int) -> JangbiResponse:
        jangbi = await self.get_1(jangbi_id)
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

    async def delete_jangbi(self, jangbi_id: int) -> JangbiResponse:
        jangbi = await self.get_1(jangbi_id)
        if not jangbi:
            return None
        jangbi_response = JangbiResponse.model_validate(jangbi)
        await self.db.delete(jangbi)
        await self.db.commit()
        return jangbi_response

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
        
        response_list = [JangbiResponse.model_validate(jangbi) for jangbi in jangbi_list]
        
        return JangbiListResponse(
            list=response_list,
            item_count=len(response_list),
            next_data_exists=next_data_exists,
            next_index=param.start_idx + len(response_list)
        )
    #--------------------------------------------
    async def add_jangbi_attachments(self, jangbi_id:int, files: List[UploadFile]) -> Boolean:
        ''' 장비에 파일 첨부 '''
        attachments = []
        async with self.db.begin() as transaction:
            try:
                parent_node_id = await self.get_jangbi_parent_node_id()
                if not parent_node_id:
                    raise ValueError("장비 부모 노드를 찾을 수 없습니다.")                
                for file in files:
                    file_uuid = str(uuid4()).replace("-", "")
                    saved_file_name = f"{file.filename}"
                    yyyymm = todayYmd()[:6]
                    base_dir = f"{config.UPLOAD_DIR_BASE}/{yyyymm}"
                    os.makedirs(base_dir, exist_ok=True)  # 해당 월 폴더 생성
                    file_location = os.path.join(base_dir, saved_file_name)

                    # 물리적 파일 저장
                    with open(file_location, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)
                        logger.debug(f"{file_location} 파일이 성공적으로 저장되었습니다.")

                    width, height = get_image_dimensions(file_location)
                    hash_code = get_file_hash(file_location)

                    url_base = config.URL_BASE
                    # 파일 URL 생성 및 추가
                    file_url = f"{url_base}/{yyyymm}/{saved_file_name}"
                    attachments.append(file_url)
                    # ApFile DB 레코드 생성
                    ap_file = ApFile(
                        node_id=file_uuid,
                        parent_node_id=parent_node_id,
                        saved_dir_name=base_dir,
                        saved_file_name=saved_file_name,
                        org_file_name=file.filename,
                        file_size=os.path.getsize(file_location),
                        content_type=file.content_type,
                        hashcode=hash_code,
                        note=None,
                        width=width,
                        height=height
                    )
                    self.db.add(ap_file)
                    # 5. MatchFileVar 저장
                    match_file_int = MatchFileInt(
                        tbl='jangbi',
                        id=jangbi_id,
                        node_id=file_uuid
                    )
                    self.db.add(match_file_int)
                await self.db.commit()
                logger.info('첨부파일 추가 성공적으로 수행되었습니다.' + file_location)
                return True
            except Exception as e:
                await transaction.rollback()
                logger.info(f"Error adding attachments to diary: {e}")
                return False

    async def get_jangbi_attachments_urls(self, jangbi_id: int) -> List[AttachFileInfo]:
        ''' 장비에 첨부된 파일의 url 목록 조회 '''
        fileService = ApNodeFileService(self.db)
        file_list = await fileService.get_file_by_match_int('jangbi', jangbi_id)
        url_base = config.URL_BASE
        result_list = []
        for file in file_list:
            saved_dir_name = file.saved_dir_name.replace('/home/kdy987/www/uploaded/','')
            url = f"{url_base}/{saved_dir_name}/{file.saved_file_name}"
            file_info = AttachFileInfo(
                node_id=file.node_id,
                file_name=file.org_file_name,
                file_size=file.file_size,
                url=url,
                width=file.width,
                height=file.height
            )
            result_list.append(file_info)
        return result_list

    async def delete_attachment(self, jangbi_id: int, node_id: str) -> dict:
        """ 장비에 첨부된 파일 1개를 삭제"""
        fileService = ApNodeFileService(self.db)

        # 트랜잭션 블록 시작
        async with self.db.begin() as transaction:
            try:
                # match_file_list에서 node_id로 조회한 후 삭제
                match_file = await fileService.get_file_by_match_int('jangbi', jangbi_id, node_id)
                # node_id로 파일 정보 조회
                node_id = match_file.node_id
                file = await fileService.get_file_by_node_id(node_id)
                if file:
                    # 실제 파일 삭제
                    os.remove(f"{file.saved_dir_name}/{file.saved_file_name}")
                    await self.db.delete(file)

                # ApFile에서 node_id로 조회한 후 삭제
                node = await fileService.get_node_by_id(node_id)
                if node:
                    await self.db.delete(node)

                # match_file 삭제
                await self.db.delete(match_file)

                # 트랜잭션이 완료되면 커밋
                await transaction.commit()

            except Exception as e:
                # 예외가 발생하면 트랜잭션 롤백
                await transaction.rollback()
                raise e

        return {"result": "success"}