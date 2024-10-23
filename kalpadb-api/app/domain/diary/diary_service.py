from sqlalchemy import asc, desc, func, literal_column  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.util import saved_path_to_url
from app.domain.diary.diary_model import Diary
from app.domain.diary.diary_schema import DiaryRequest, DiaryListResponse
from app.domain.filenode.filenode_model import ApFile, MatchFileVar
from app.domain.filenode.filenode_service import ApNodeFileService
from app.core.logger import get_logger

logger = get_logger(__name__)
class DiaryService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # Create
    async def create_diary(self, diary_data: DiaryRequest) -> DiaryListResponse:
        new_diary = Diary(
            ymd=diary_data.ymd,
            content=diary_data.content,
            summary=diary_data.summary
        )
        self.db.add(new_diary)
        await self.db.commit()
        await self.db.refresh(new_diary)
        return DiaryListResponse.model_validate(new_diary)

    # Read
    async def get_diary(self, ymd: str) -> DiaryListResponse | None:
        result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
        diary = result.scalar_one_or_none()  # 일치하는 첫 번째 결과를 가져옴
        if not diary:
            return None
        fileService = ApNodeFileService(self.db)
        file_list = await fileService.get_file_by_match('dairy', ymd)
        if file_list:
            image_paths = [f"{imgfile.saved_dir_name}/{imgfile.saved_file_name}" for imgfile in file_list]
            diary.attachments = saved_path_to_url( ','.join(image_paths) )

        if diary:
            return DiaryListResponse.model_validate(diary)
        return None

    # Update
    async def update_diary(self, ymd: str, diary_data: DiaryRequest) -> DiaryListResponse | None:
        result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
        diary = result.scalar_one_or_none()
        if diary:
            diary.content = diary_data.content
            diary.summary = diary_data.summary
            await self.db.commit()
            await self.db.refresh(diary)
            return DiaryListResponse.model_validate(diary)
        return None

    # Delete
    async def delete_diary(self, ymd: str) -> bool:
        ''' 일기 1개를 삭제 일기가 존재하지 않거나 삭제 실패시 false를, 삭제를 하면 true를 반환 '''
        try:
            # Diary 삭제 대상 조회
            result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
            diary = result.scalar_one_or_none()

            if not diary:
                return False  # Diary가 없으면 False 반환

            # MatchFileVar 삭제 (MatchFileVar에 데이터가 있을 수도, 없을 수도 있음)
            result = await self.db.execute(
                select(MatchFileVar).filter(MatchFileVar.tbl == 'dairy', MatchFileVar.id == ymd)
            )
            match_file_vars = result.scalars().all()

            if match_file_vars:
                # MatchFileVar 레코드 삭제
                for match_file_var in match_file_vars:
                    await self.db.delete(match_file_var)

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
        self, start_ymd: str, end_ymd: str, start_index: int, limit: int, order: str, summary_only: bool = False
    ) -> dict:
        ''' Paging 이미지 포함 '''
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

        return {
            "data": data,
            "next_data_exists": next_data_exists,
            "last_index": last_index
        }

