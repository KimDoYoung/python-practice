#!/bin/bash

# Lock 파일이 있으면 삭제
if [ -f /data/db/mongod.lock ]; then
    rm /data/db/mongod.lock
    echo "Removed mongod.lock"
fi

# MongoDB 실행
mongod --bind_ip_all &

# MongoDB가 준비될 때까지 대기
sleep 10

echo "MongoDB 기동 완료. Import 시작..."

# Import 명령어 수행 (중복 문서 오류 방지)
mongoimport --host localhost --db ipo-scheduler --collection Config --file /data/import/Config.json --jsonArray --mode=upsert || echo "Config import 실패"
mongoimport --host localhost --db ipo-scheduler --collection SchedulerJob --file /data/import/SchedulerJob.json --jsonArray --mode=upsert || echo "SchedulerJob import 실패"
mongoimport --host localhost --db ipo-scheduler --collection Users --file /data/import/Users.json --jsonArray --mode=upsert || echo "Users import 실패"
mongoimport --host localhost --db ipo-scheduler --collection EventDays --file /data/import/EventDays.json --jsonArray --mode=upsert || echo "EventDays import 실패"
mongoimport --host localhost --db ipo-scheduler --collection Ipo --file /data/import/Ipo.json --jsonArray --mode=upsert || echo "Ipo import 실패"
mongoimport --host localhost --db ipo-scheduler --collection IpoHistory --file /data/import/IpoHistory.json --jsonArray --mode=upsert || echo "IpoHistory import 실패"

# MongoDB를 백그라운드에서 계속 실행
tail -f /dev/null
