
import traceback
from typing import List, Optional

from sqlalchemy import select, text
from backend.app.domain.ifi.ifi05.ifi05_job_schedule_model import Ifi05JobSchedule
from backend.app.domain.ifi.ifi05.ifi05_job_schedule_schema import Ifi05JobScheduleCreate, Ifi05JobScheduleResponse
from backend.app.core.database import get_session
from backend.app.core.logger import get_logger

logger = get_logger()

class Ifi05Service:

    @staticmethod
    async def generate_id() -> Optional[int]:
        """ ID 생성"""
        async with get_session() as session:
            result = await session.execute(text("SELECT f_create_seq()"))
            return result.scalar()
        
    @staticmethod
    async def list_all() -> List[Ifi05JobScheduleResponse]:
        """회사 API ID 생성"""
        async with get_session() as session:
            query = select(Ifi05JobSchedule)
            result = await session.execute(query)
            list_ifi05 = result.scalars().all()
            return [Ifi05JobScheduleResponse.model_validate(job) for job in list_ifi05]
    
    @staticmethod
    async def get_1(id: int) -> Ifi05JobScheduleResponse:
        ''' id로 1개의 ifi05_job_schedule 조회 '''
        async with get_session() as session:
            query = select(Ifi05JobSchedule).where(Ifi05JobSchedule.ifi05_job_schedule_id == id)
            result = await session.execute(query)
            ifi05 = result.scalars().first()
            return Ifi05JobScheduleResponse.model_validate(ifi05)
        
    @staticmethod
    async def create(request: Ifi05JobScheduleCreate) -> Ifi05JobSchedule:
        ''' ifi05_job_schedule 생성 '''
        dict_data = request.model_dump()
        dict_data['ifi05_job_schedule_id'] = await Ifi05Service.generate_id()
        
        async with get_session() as session:
            ifi05 = Ifi05JobSchedule(**dict_data)
            session.add(ifi05)
            await session.commit()
            return ifi05

    @staticmethod
    async def delete(id: int) -> Ifi05JobSchedule:
        ''' ifi05_job_schedule 삭제 '''
        async with get_session() as session:
            query = select(Ifi05JobSchedule).where(Ifi05JobSchedule.ifi05_job_schedule_id == id)
            result = await session.execute(query)
            ifi05 = result.scalar_one_or_none()
            if ifi05 is None:
                logger.warning("삭제할 레코드를 찾을 수 없습니다.")
                raise Exception("삭제할 레코드를 찾을 수 없습니다.")
            try:
                await session.delete(ifi05)
                await session.commit()
                logger.info(f'{id} 삭제 성공')
            except Exception as e:
                logger.error(f"삭제 중 예외 발생: {e}")
                traceback.print_exc()
                raise Exception("삭제 중 예외 발생")
            
            return ifi05

    @staticmethod
    async def update(update_data: Ifi05JobScheduleResponse) -> Ifi05JobScheduleResponse:
        """ifi05_job_schedule 수정"""
        async with get_session() as session:
            query = select(Ifi05JobSchedule).where(Ifi05JobSchedule.ifi05_job_schedule_id == update_data.ifi05_job_schedule_id)
            result = await session.execute(query)
            ifi05 = result.scalar_one_or_none()
            
            if ifi05 is None:
                logger.warning("수정할 레코드를 찾을 수 없습니다.")
                raise Exception("수정할 레코드를 찾을 수 없습니다.")
            
            try:
                # `update_data`의 속성을 `ifi05` 객체에 업데이트
                update_dict = update_data.model_dump(exclude_unset=True)  # Pydantic 모델에서 변경된 데이터만 가져옴
                for key, value in update_dict.items():
                    setattr(ifi05, key, value)  # 각 속성 업데이트

                await session.commit()
                logger.info(f'{update_data.ifi05_job_schedule_id} 수정 성공')
            except Exception as e:
                logger.error(f"수정 중 예외 발생: {e}")
                traceback.print_exc()
                raise Exception("수정 중 예외 발생")
            
            # 수정된 데이터를 Ifi05JobScheduleResponse로 반환
            return Ifi05JobScheduleResponse.model_validate(ifi05)
        