from sqlalchemy import asc, desc, func, literal_column  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.diary.diary_model import Diary
from app.domain.diary.diary_schema import DiaryRequest, DiaryListResponse
from app.domain.filenode.filenode_model import ApFile, MatchFileVar

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
        result = await self.db.execute(select(Diary).filter(Diary.ymd == ymd))
        diary = result.scalar_one_or_none()
        if diary:
            await self.db.delete(diary)
            await self.db.commit()
            return True
        return False

    # Read with pagination, date range, and summary_only option
    async def get_diaries1(
        self, start_ymd: str, end_ymd: str, start_index: int, limit: int, order: str, summary_only: bool = False
    ) -> dict:
        sort_order = asc(Diary.ymd) if order == 'asc' else desc(Diary.ymd)

        # 기본 SQL 쿼리 작성
        stmt = (
            select(Diary)
            .where(Diary.ymd >= start_ymd)
            .where(Diary.ymd <= end_ymd)
            .order_by(sort_order)
            .offset(start_index)
            .limit(limit + 1)  # +1을 통해 다음 데이터가 있는지 확인
        )

        result = await self.db.execute(stmt)
        diaries = result.scalars().all()

        next_data_exists = 'Y' if len(diaries) > limit else 'N'
        diaries = diaries[:limit]
        last_index = start_index + len(diaries)

        # summary_only가 True일 경우, summary만 반환하도록 함
        if summary_only:
            data = [{"ymd": diary.ymd, "summary": diary.summary} for diary in diaries]
        else:
            data = [DiaryListResponse.model_validate(diary) for diary in diaries]

        return {
            "data": data,
            "next_data_exists": next_data_exists,
            "last_index": last_index
        }

    async def get_diaries(
        self, start_ymd: str, end_ymd: str, start_index: int, limit: int, order: str, summary_only: bool = False
    ) -> dict:
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

        # files 경로를 변환하는 함수
        def convert_to_url(files_str):
            base_url = "http://jskn.iptime.org:6789/uploaded/"
            if not files_str:
                return None
            # 파일 경로를 쉼표로 나눈 후, /home/kdy987/www/ 부분을 제거하고 URL로 변환
            files = files_str.split(",")
            # 빈 문자열을 제거하고 경로를 변환하여 리스트에 추가
            return [base_url + file.strip().replace("/home/kdy987/www/uploaded/", "") 
                    for file in files if file.strip()]

        # 데이터 처리
        if summary_only:
            data = [{"ymd": diary.ymd, "summary": diary.summary} for diary in diaries]
        else:
            data = []
            for diary in diaries:
                # files를 URL 리스트로 변환
                attachments = convert_to_url(diary.files)

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

