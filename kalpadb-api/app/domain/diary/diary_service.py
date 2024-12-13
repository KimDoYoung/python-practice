# diary_service.py
"""
모듈 설명: 
    - 일기 관련 비즈니스 로직 처리
주요 기능:
    - create_diary : 일기 생성
    - get_diary : 일기 조회
    - update_diary : 일기 수정
    - delete_diary : 일기 삭제
    - get_diaries : 일기 목록 조회
    - get_diary_attachments_urls : 일기에 첨부된 파일 URL 목록 조회
    - get_diary_delete_attachment : 일기에 첨부된 파일 1개 삭제

작성자: 김도영
작성일: 2024-10-27
버전: 1.0
"""
import os
import shutil
from typing import List
from uuid import uuid4
from sqlalchemy import Boolean, asc, desc, func, literal_column  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.util import get_file_hash, get_image_dimensions, saved_path_to_url
from app.domain.diary.diary_model import Diary
from app.domain.diary.diary_schema import DiaryPageModel, DiaryBase, DiaryDetailResponse, DiaryRequest, DiaryListResponse, DiaryResponse, DiaryUpdateRequest
from app.domain.filenode.filenode_model import ApFile, ApNode, MatchFileVar
from app.domain.filenode.filenode_schema import AttachFileInfo, FileNoteData
from app.domain.filenode.filenode_service import ApNodeFileService
from fastapi import File, UploadFile
from app.core.logger import get_logger
from app.core.settings import config

logger = get_logger(__name__)
class DiaryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def upsert_diary(self, diary_data: DiaryRequest) -> DiaryResponse:
        ''' 일기 생성 이미지 첨부 없이 추가 가능'''
        result = await self.db.execute(select(Diary).filter(Diary.ymd == diary_data.ymd))
        diary = result.scalar_one_or_none()  # 일치하는 첫 번째 결과를 가져옴
        if not diary:            
            diary = Diary(
                ymd=diary_data.ymd,
                content=diary_data.content,
                summary=diary_data.summary
            )
            self.db.add(diary)
        else:
            diary.content = diary_data.content
            diary.summary = diary_data.summary
        await self.db.commit()
        await self.db.refresh(diary)
        return DiaryResponse(
            ymd=diary.ymd,
            content=diary.content,
            summary=diary.summary
        )
    # Create
    async def create_diary(self, diary_data: DiaryRequest, files: List[UploadFile] = File(None) ) -> DiaryResponse:
        ''' 일기 생성 이미지 첨부 없이 추가 가능'''
        diary = Diary(
            ymd=diary_data.ymd,
            content=diary_data.content,
            summary=diary_data.summary
        )

        # 나머지 작업을 트랜잭션으로 처리
        async with self.db.begin() as transaction:
            try:
                self.db.add(diary)
                await self.db.commit()
                if files is None:
                    return DiaryResponse(
                        ymd=diary.ymd,
                        content=diary.content,
                        summary=diary.summary,
                        attachments=[]
                    )                
                # 2. ApNode 조회하여 이미지 저장할 Node가 있는지 확인
                yyyymm = diary_data.ymd[:6]  # 'yyyymm' 형식 추출
                node_name = yyyymm

                parent_node_query = select(ApNode.id).where(
                    (ApNode.node_type == 'D') & 
                    (ApNode.name == '일기')
                ).limit(1)

                parent_node_result = await self.db.execute(parent_node_query)
                parent_node_id = parent_node_result.scalar_one_or_none()

                if not parent_node_id:
                    raise ValueError("일기 부모 노드를 찾을 수 없습니다.")

                # Node의 존재 여부 확인
                node_query = select(ApNode.id).where(
                    (ApNode.node_type == 'D') & 
                    (ApNode.parent_id == parent_node_id) & 
                    (ApNode.name == node_name)
                )
                node_result = await self.db.execute(node_query)
                node_id = node_result.scalar_one_or_none()

                # 3. Node가 없으면 새로 생성
                # base_dir = f"/home/kdy987/uploaded/일기/"
                base_dir = config.UPLOAD_DIR_BASE
                if not node_id:
                    node_id = str(uuid4()).replace("-", "")
                    new_node = ApNode(
                        id=node_id,
                        node_type='D',
                        parent_id=parent_node_id,
                        name=node_name,
                        full_name=f"{base_dir}/{node_name}",
                        owner_id='kdy987',
                        group_auth=755,
                        guest_auth=755,
                        delete_yn='N'
                    )
                    self.db.add(new_node)
                    await self.db.flush()  # 새로 생성된 노드 ID를 트랜잭션 내에서 사용할 수 있도록 확정

                # 4. ApFile 저장 및 파일 물리적으로 저장
                attachments = []
                #base_dir = f"/home/kdy987/www/uploaded/{yyyymm}"
                base_dir = f"{config.UPLOAD_DIR_BASE}/{yyyymm}"
                os.makedirs(base_dir, exist_ok=True)  # 해당 월 폴더 생성

                for file in files:
                    file_uuid = str(uuid4()).replace("-", "")
                    saved_file_name = f"{file.filename}"
                    file_location = os.path.join(base_dir, saved_file_name)
                    
                    # 물리적 파일 저장
                    with open(file_location, "wb") as buffer:
                        shutil.copyfileobj(file.file, buffer)

                    width, height = get_image_dimensions(file_location)
                    hash_code = get_file_hash(file_location)

                    url_base = config.URL_BASE 
                    # 파일 URL 생성 및 추가
                    file_url = f"{url_base}/{yyyymm}/{saved_file_name}"
                    attachments.append(file_url)

                    # ApFile DB 레코드 생성
                    ap_file = ApFile(
                        node_id=file_uuid,
                        parent_node_id=node_id,
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
                    match_file_var = MatchFileVar(
                        tbl='dairy',
                        id=diary_data.ymd,
                        node_id=file_uuid
                    )
                    self.db.add(match_file_var)

                # 트랜잭션 커밋
                await self.db.commit()

            except Exception as e:
                # 오류가 발생하면 롤백
                await transaction.rollback()
                print(f"Error creating diary and related entries: {e}")
                return None

        # 최종 응답 생성
        diary_response = DiaryResponse(
            ymd=diary.ymd,
            content=diary.content,
            summary=diary.summary,
            attachments=attachments
        )
        
        return diary_response
    
    # Read
    async def get_diary(self, ymd: str) -> DiaryDetailResponse | None:
        ''' diary 1개 조회, 달려있는 이미지 리스트도 함께 조회 '''
        result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
        diary = result.scalar_one_or_none()  # 일치하는 첫 번째 결과를 가져옴
        if not diary:
            return None
        fileService = ApNodeFileService(self.db)
        file_list = await fileService.get_file_by_match('dairy', ymd)
        attachs = []
        if file_list:
            for imgfile in file_list:
                saved_dir_name = imgfile.saved_dir_name.replace('/home/kdy987/www/uploaded/','')
                url = f"{config.URL_BASE}/{saved_dir_name}/{imgfile.saved_file_name}"
                attachs.append({
                    "node_id": imgfile.node_id,
                    "org_file_name": imgfile.org_file_name,
                    "file_size": imgfile.file_size,
                    "url": url,
                    "width" : imgfile.width,
                    "height" : imgfile.height
                })
        found_diary = DiaryDetailResponse.model_validate(diary)
        found_diary.attachments = attachs
        return found_diary

    # Update
    async def update_diary(self, ymd: str, diary_data: DiaryUpdateRequest) -> DiaryBase | None:
        ''' diary 1개 수정, 수정된 diary를 반환, diary가 존재하지 않으면 None 반환 '''
        result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
        diary = result.scalar_one_or_none()
        if diary:
            diary.content = diary_data.content
            diary.summary = diary_data.summary
            await self.db.commit()
            await self.db.refresh(diary)
            return DiaryBase.model_validate(diary.__dict__)
        return None

    # Delete
    async def delete_diary(self, ymd: str) -> bool:
        ''' 일기 1개를 삭제, 일기가 존재하지 않거나 삭제 실패 시 False를, 삭제를 완료하면 True를 반환 '''
        try:
            # Diary 삭제 대상 조회
            result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
            diary = result.scalar_one_or_none()

            if not diary:
                return False  # Diary가 없으면 False 반환

            # MatchFileVar에서 해당 일기에 연결된 파일들 조회
            result = await self.db.execute(
                select(MatchFileVar).filter(MatchFileVar.tbl == 'diary', MatchFileVar.id == ymd)
            )
            match_file_vars = result.scalars().all()

            # 각 MatchFileVar와 연결된 ApFile, ApNode 삭제
            for match_file_var in match_file_vars:
                # ApFile 조회 및 삭제
                file_result = await self.db.execute(
                    select(ApFile).filter(ApFile.parent_node_id == match_file_var.node_id)
                )
                ap_files = file_result.scalars().all()

                for ap_file in ap_files:
                    # ApNode 조회 및 삭제
                    node_result = await self.db.execute(
                        select(ApNode).filter(ApNode.parent_id == ap_file.parent_node_id)
                    )
                    ap_nodes = node_result.scalars().all()

                    for ap_node in ap_nodes:
                        await self.db.delete(ap_node)  # ApNode 삭제

                    await self.db.delete(ap_file)  # ApFile 삭제

                await self.db.delete(match_file_var)  # MatchFileVar 삭제

            # Diary 레코드 삭제
            await self.db.delete(diary)

            # 트랜잭션 커밋
            await self.db.commit()

            return True

        except Exception as e:
            await self.db.rollback()
            logger.info(f"일기 삭제 중 오류가 발생했습니다: {e}")
            return False

    async def get_diaries(
        self, start_ymd: str, end_ymd: str, 
        start_index: int, limit: int, 
        order: str, summary_only: bool = False,
        search_text: str = ""
    ) -> DiaryPageModel:
        ''' diary Paging 이미지 포함 '''
        # 정렬 순서 설정
        sort_order = asc(Diary.ymd) if order == 'asc' else desc(Diary.ymd)
        
        # 쿼리 작성
        query = (
            select(
                Diary.ymd,
                Diary.summary,
                Diary.content,
                func.group_concat(
                    func.concat(ApFile.saved_dir_name, '/', ApFile.saved_file_name),
                    literal_column("','")  # 쉼표와 공백으로 구분
                ).label('files')
            )
            .outerjoin(MatchFileVar, (Diary.ymd == MatchFileVar.id) & (MatchFileVar.tbl == 'dairy'))
            .outerjoin(ApFile, MatchFileVar.node_id == ApFile.node_id)
            .where(Diary.ymd >= start_ymd)
            .where(Diary.ymd <= end_ymd)
            .where(Diary.content.contains(search_text) | Diary.summary.contains(search_text))
            .group_by(Diary.ymd, Diary.summary, Diary.content)
            .order_by(sort_order)
            .offset(start_index)
            .limit(limit + 1)  # 다음 페이지 데이터가 있는지 확인하기 위해 limit + 1
        )

        # 쿼리 실행
        result = await self.db.execute(query)
        diaries = result.fetchall()

        # 다음 데이터가 있는지 여부 확인
        next_data_exists = 'Y' if len(diaries) > limit else 'N'
        diaries = diaries[:limit]  # 실제 데이터는 limit만큼만 사용
        last_index = start_index + len(diaries)
        data_count = len(diaries)

        # 데이터 처리
        if summary_only:
            data = [{"ymd": diary.ymd, "summary": diary.summary} for diary in diaries]
        else:
            data = []
            for diary in diaries:
                # files를 URL 리스트로 변환
                attachments = saved_path_to_url(diary.files)

                # Pydantic 모델로 변환
                diary_response = DiaryListResponse(
                    ymd=diary.ymd,
                    content=diary.content,
                    summary=diary.summary,
                    attachments=attachments
                )
                data.append(diary_response)
        return DiaryPageModel(
            data=data,
            data_count=data_count,
            next_data_exists=next_data_exists,
            start_index=start_index,
            last_index=last_index,
            limit=limit,
            start_ymd=start_ymd,
            end_ymd=end_ymd,
            order=order            
        )
    
    async def get_diary_parent_node_id(self) -> str:
        ''' 일기 부모 노드 ID 조회 '''
        parent_node_query = select(ApNode.id).where(
            (ApNode.node_type == 'D') & 
            (ApNode.name == '일기')
        ).limit(1)

        parent_node_result = await self.db.execute(parent_node_query)
        parent_node_id = parent_node_result.scalar_one_or_none() 
        return parent_node_id

    async def add_diary_attachments(self, ymd:str, files: List[UploadFile]) -> Boolean:
        ''' 일지에 파일 첨부 '''
        attachments = []
        async with self.db.begin() as transaction:
            try:
                parent_node_id = await self.get_diary_parent_node_id()
                if not parent_node_id:
                    raise ValueError("일기 부모 노드를 찾을 수 없습니다.")                
                for file in files:
                    file_uuid = str(uuid4()).replace("-", "")
                    saved_file_name = f"{file.filename}"
                    yyyymm = ymd[:6]
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
                    match_file_var = MatchFileVar(
                        tbl='dairy',
                        id=ymd,
                        node_id=file_uuid
                    )
                    self.db.add(match_file_var)
                await self.db.commit()
                logger.info('첨부파일 추가 성공적으로 수행되었습니다.' + file_location)
                return True
            except Exception as e:
                await transaction.rollback()
                logger.info(f"Error adding attachments to diary: {e}")
                return False

    async def get_diary_attachments_urls(self, ymd: str) -> List[AttachFileInfo]:
        ''' 일지에 첨부된 파일의 url 목록 조회 '''
        fileService = ApNodeFileService(self.db)
        file_list = await fileService.get_file_by_match('dairy', ymd)
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
            

    async def get_diary_delete_attachment(self, ymd: str, node_id: str) -> dict:
        """일지에 첨부된 파일 1개를 삭제"""
        fileService = ApNodeFileService(self.db)

        # 트랜잭션 블록 시작
        async with self.db.begin() as transaction:
            try:
                # match_file_list에서 node_id로 조회한 후 삭제
                match_file = await fileService.get_file_in_match_by_id_and_node_id('dairy', ymd, node_id)
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
    
    async def set_diary_attachment_note(self, note_data: FileNoteData) -> ApFile:
        fileService = ApNodeFileService(self.db)
        return await fileService.set_note(note_data.node_id, note_data.note)

