from functools import lru_cache

@lru_cache()
def get_user_service():
    from backend.app.domains.user.user_service import UserService
    return UserService()

@lru_cache()
def get_eventdays_service():
    from backend.app.domains.system.eventdays_service import EventDaysService
    return EventDaysService()

@lru_cache()
def get_ipo_service():
    from backend.app.domains.ipo.ipo_service import IpoService
    return IpoService()

@lru_cache()
def get_ipohistory_service():
    from backend.app.domains.ipo.ipo_history_service import IpoHistoryService
    return IpoHistoryService()

@lru_cache()
def get_config_service():
    from backend.app.domains.system.config_service import DbConfigService
    return DbConfigService()

@lru_cache()
def get_scheduler_job_service():
    from backend.app.domains.system.scheduler_job_service import SchedulerJobService
    from backend.app.core.scheduler import Scheduler
    scheduler = Scheduler.get_instance() 
    return SchedulerJobService(scheduler=scheduler)

@lru_cache()
def get_log_service():
    from backend.app.domains.system.logs_service import LogsService
    return LogsService()
