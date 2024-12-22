# extutil_service.py
"""
모듈 설명: 
    - External Util Service
주요 기능:
    - 

작성자: 김도영
작성일: 2024-12-22
버전: 1.0
"""
from typing import List
from korean_lunar_calendar import KoreanLunarCalendar
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import get_logger
from app.domain.extutil.extutil_schema import SolarLunarResponse

logger = get_logger(__name__)

class ExtUtilService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def solYmd2lunYmd(self, solYmd):
        ''' 1개의 양력 날짜를 음력 날짜로 변환 '''
        calendar = KoreanLunarCalendar()
        y = int(solYmd[:4])
        M = int(solYmd[4:6])
        d = int(solYmd[6:])

        calendar.setSolarDate(y, M, d)

        # Lunar Date (ISO Format)
        lunarDate = calendar.LunarIsoFormat().replace('-', '') # 20201208
        logger.debug(f"solYmd2lunYmd: {solYmd} -> {lunarDate}")
        return lunarDate
    
    def sol2lun_array(self, ymd_array) -> List[SolarLunarResponse]:
        ''' 배열에 담긴 양력 날짜를 음력 날짜로 변환 '''
        lunYmdArray = []
        for solYmd in ymd_array:
            lunYmd = self.solYmd2lunYmd(solYmd)
            sol_lun_response = SolarLunarResponse(solYmd=solYmd, lunYmd=lunYmd)
            lunYmdArray.append(sol_lun_response)
        return lunYmdArray
    
    def last_yyyymmdd(self, yyyymm: str) -> str:
        ''' 해당 월의 마지막 날짜 yyyymmdd 반환 '''
        year = yyyymm[:4]
        month = yyyymm[4:]
        if month == '02':
            if int(year) % 4 == 0:
                return year + month + '29'
            else:
                return year + month + '28'
        elif month in ['04', '06', '09', '11']:
            return year + month + '30'
        else:
            return year + month + '31'
