# scheduler.py
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from typing import Any, Callable, Dict, List

import pytz
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

class Scheduler:
    ''' 스케줄러 클래스 : singleton으로 동작 '''
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Scheduler, cls).__new__(cls)
            cls._instance.scheduler = BackgroundScheduler(timezone=pytz.timezone("Asia/Seoul"))
            
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance    

    def start(self):
        try:
            if not self.scheduler.running:
                self.scheduler.start()
                return {"message": "Scheduler started successfully"}
            else:
                return {"message": "Scheduler is already running"}
        except Exception as e:
            return {"error": str(e)}

    def add_cron_job(self, func: Callable, cron: str, job_id: str,  args: tuple = (),  max_instances: int = 1) -> None:
        try:
            logger.debug('add_cron_job 함수 실행:' + job_id)
            job = self.scheduler.add_job(func, CronTrigger.from_crontab(cron), id=job_id, args=args, max_instances=max_instances)
            logger.debug('add_cron_job 함수 실행 완료:' + job_id)
        except Exception as e:
            logger.error(f'Error adding job {job_id}: {e}', exc_info=True)
            return {"error": str(e)}   

    def add_date_job(self, func: Callable, run_date: datetime, job_id: str, job_type:str, args: tuple = ()) -> None:
        try:
            job = self.scheduler.add_job(func, DateTrigger(run_date=run_date), id=job_id, args=args)
        except Exception as e:
            return {"error": str(e)}

    def get_jobs(self) -> List[Dict[str, Any]]:
        return self.scheduler.get_jobs()
    
    def remove_job(self, job_id: str):
        try:
            self.scheduler.remove_job(job_id)
            return {"message": "Job removed successfully"}
        except Exception as e:
            return {"error": str(e)}

    def shutdown(self):
        try:
            self.scheduler.shutdown()
            return {"message": "Scheduler shut down successfully"}
        except Exception as e:
            return {"error": str(e)}

    def stop(self):
        try:
            if self.scheduler.running:
                self.scheduler.pause()
                return {"message": "Scheduler paused successfully"}
            else:
                return {"message": "Scheduler is not running"}
        except Exception as e:
            return {"error": str(e)}

    def restart(self):
        try:
            if not self.scheduler.running:
                return {"message": "Scheduler is not running"}
            elif self.scheduler.state == 0:  # APScheduler.STATE_STOPPED = 0
                self.scheduler.resume()
                return {"message": "Scheduler resumed successfully"}
            else:
                return {"message": "Scheduler is already running"}
        except Exception as e:
            return {"error": str(e)}
    