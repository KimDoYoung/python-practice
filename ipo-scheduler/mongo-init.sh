#!/bin/bash

# Lock 파일이 있으면 삭제
if [ -f /data/db/mongod.lock ]; then
    rm /data/db/mongod.lock
    echo "Removed mongod.lock"
fi

# MongoDB 실행
mongod --bind_ip_all &

# MongoDB 프로세스 확인
if [ $? -ne 0 ]; then
    echo "MongoDB 실행 실패"
    exit 1
fi

# MongoDB가 준비될 때까지 대기
RETRIES=5
until mongo --host localhost --eval 'print("MongoDB is ready")' || [ $RETRIES -eq 0 ]; do
    echo "MongoDB가 아직 준비되지 않았습니다. 대기 중..."
    RETRIES=$((RETRIES - 1))
    sleep 5
done

if [ $RETRIES -eq 0 ]; then
    echo "MongoDB 준비 실패"
    exit 1
fi

echo "MongoDB 기동 완료. Import 시작..."

# Import 명령어 수행 (중복 문서 오류 방지)
if ! mongo ipo-scheduler --eval 'db.Config.findOne()'; then
    echo "데이터를 Import합니다."
    mongoimport --host localhost --db ipo-scheduler --collection Config --file /data/import/Config.json --jsonArray --mode=upsert || echo "Config import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection SchedulerJob --file /data/import/SchedulerJob.json --jsonArray --mode=upsert || echo "SchedulerJob import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection Users --file /data/import/Users.json --jsonArray --mode=upsert || echo "Users import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection EventDays --file /data/import/EventDays.json --jsonArray --mode=upsert || echo "EventDays import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection Ipo --file /data/import/Ipo.json --jsonArray --mode=upsert || echo "Ipo import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection IpoHistory --file /data/import/IpoHistory.json --jsonArray --mode=upsert || echo "IpoHistory import 실패"
fi
# MongoDB 프로세스를 백그라운드에서 유지
wait
