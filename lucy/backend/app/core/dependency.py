from backend.app.core.mongodb import MongoDb
from backend.app.domains.system.config_service import DbConfigService
from backend.app.domains.system.eventdays_service import EventDaysService
from backend.app.domains.system.ipo_service import IpoService
from backend.app.domains.system.scheduler_job_service import SchedulerJobService
from backend.app.domains.user.user_service import UserService
from backend.app.core.scheduler import Scheduler


def get_user_service() -> UserService:
    return UserService(MongoDb.get_client()["stockdb"])

def get_eventdays_service() -> EventDaysService:
    return EventDaysService(MongoDb.get_client()["stockdb"])

def get_ipo_service() -> IpoService:
    return IpoService(MongoDb.get_client()["stockdb"])

def get_config_service() -> DbConfigService:
    return DbConfigService(MongoDb.get_client()["stockdb"])

def get_scheduler_job_service() -> SchedulerJobService:
    scheduler = Scheduler.get_instance()
    return SchedulerJobService(scheduler=scheduler)
