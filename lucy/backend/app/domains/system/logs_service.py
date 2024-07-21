from datetime import datetime, timedelta
from backend.app.domains.system.logs_model import Logs


class LogsService:

    async def create_log(self, gubun: str, level: str, title: str, detail: str):
        log = Logs(gubun=gubun, level=level, title=title, detail=detail)
        await log.create()

    async def danta_info(self, title: str, detail: str):
        await self.create_log(gubun="Danta", level="Info", title=title, detail=detail)

    async def danta_error(self, title: str, detail: str):
        await self.create_log(gubun="Danta", level="Error", title=title, detail=detail)

    async def cron_info(self, title: str, detail: str):
        await self.create_log(gubun="Cron", level="Info", title=title, detail=detail)

    async def cron_error(self, title: str, detail: str):
        await self.create_log(gubun="Cron", level="Error", title=title, detail=detail)

    async def get_all(self):
        logs = await Logs.find().sort(-Logs.upd_time).to_list()
        return logs
    
    async def get_logs_by_date(self, ymd: str):
        # yyyyMMdd 형식의 문자열을 datetime 객체로 변환
        date = datetime.strptime(ymd, "%Y%m%d")
        start_of_day = datetime(date.year, date.month, date.day)
        end_of_day = start_of_day + timedelta(days=1)
        
        logs = await Logs.find(Logs.upd_time >= start_of_day, Logs.upd_time < end_of_day).sort(-Logs.upd_time).to_list()
        return logs