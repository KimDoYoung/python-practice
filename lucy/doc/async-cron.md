# async함수를 cron으로 등록하기

## 질문
async def site38_work():
    '''
    1. delete collection 'ipo_scrap_38' in mongodb
    2. call scrapping_38_fill_ipo_38 in s38_2 function
    3. 성공시 delete 'Ipo' collection in mongodb
    4. call scrap38_2_ipo in f38_2  (Ipo collection으로 옮기기)
    '''
이 함수를 BackgroundScheduler 로  cron으로 등록해서 즉 월화수목금 5일의 오전6시에 수행시킬려고해
async함수인데 가능할까?

```python
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from s38_2 import scrapping_38_fill_ipo_38, scrap38_2_ipo
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB 설정
MONGO_URI = 'mongodb://localhost:27017'
DATABASE_NAME = 'your_database_name'

async def site38_work():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DATABASE_NAME]

    # 1. Delete collection 'ipo_scrap_38'
    await db['ipo_scrap_38'].drop()

    # 2. Call scrapping_38_fill_ipo_38
    await scrapping_38_fill_ipo_38()

    # 3. 성공 시 delete 'Ipo' collection
    await db['Ipo'].drop()

    # 4. Call scrap38_2_ipo
    await scrap38_2_ipo()

    client.close()

def run_async_job(async_func):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_func())

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    
    # 월화수목금 오전 6시에 수행하도록 cron job 등록
    scheduler.add_job(run_async_job, 'cron', day_of_week='mon-fri', hour=6, minute=0, args=[site38_work])

    scheduler.start()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
```