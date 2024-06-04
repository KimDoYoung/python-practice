from backend.app.background.jobs.f38_2 import  work1
from backend.app.background.jobs.s38_2 import scrapping_38_fill_ipo_38
from backend.app.core.mongodb import MongoDb
from backend.app.core.config import config
from backend.app.core.logger import get_logger

logger = get_logger(__name__)

async def site38_work():
    '''
    1. delete collection 'ipo_scrap_38' in mongodb
    2. call scrapping_38_fill_ipo_38 in s38_2 function
    3. 성공시 delete 'Ipo' collection in mongodb
    4. call scrap38_2_ipo in f38_2  (Ipo collection으로 옮기기)
    '''
    # 1. delete collection 'ipo_scrap_38' in mongodb
    logger.info('*******************************************')
    logger.info('site38_work() start')
    logger.info('*******************************************')

    client = MongoDb.get_client()
    db_name = config.DB_NAME;
    db = client[db_name]
    collection = db['ipo_scrap_38']
    collection.delete_many({})
    
    # 2. call scrapping_38_fill_ipo_38 in s38_2 function
    logger.info('-----------------------------------------------')
    logger.info('Calling scrapping_38_fill_ipo_38()')
    logger.info('-----------------------------------------------')
    result =  scrapping_38_fill_ipo_38()
    logger.info('-----------------------------------------------')
    logger.info('scrapping_38_fill_ipo_38() returned %s', result)
    logger.info('-----------------------------------------------')
    if not result:
        collection = db['Config']
        collection.delete_one({'key':'site38_work'})        
        logger.error('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        logger.error('scrapping_38_fill_ipo_38 failed')
        logger.error('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        return False
    
    # 3. 성공시 delete 'Ipo' collection in mongodb
    logger.info('-----------------------------------------------')
    logger.info('Deleting collection Ipo')
    logger.info('-----------------------------------------------')
    collection = db['Ipo']
    collection.delete_many({})

    # 4. call scrap38_2_ipo in f38_2  (Ipo collection으로 옮기기)
    logger.info('-----------------------------------------------')
    logger.info('calling  work1 of f38_2()')
    logger.info('-----------------------------------------------')
    # scrap38_2_ipo(db, True)
    await work1(db, True)

    logger.info('Config의 key site38_work 삭제')
    collection = db['Config']
    collection.delete_one({'key':'site38_work'})

    logger.info('*******************************************')
    logger.info('site38_work() end')
    logger.info('*******************************************')
