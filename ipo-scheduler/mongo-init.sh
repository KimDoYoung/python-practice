#!/bin/bash

# -----------------------------------------------------------------------------
# mongo-init.sh
# -----------------------------------------------------------------------------

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

echo "MongoDB 기동 완료. Database 확인 중..."

# ipo-scheduler 데이터베이스 존재 여부 확인 후 Import 수행
if ! mongo --quiet --eval 'db.getMongo().getDBNames().indexOf("ipo-scheduler") >= 0'; then
    echo "ipo-scheduler 데이터베이스가 없으므로 데이터를 Import합니다."
    mongoimport --host localhost --db ipo-scheduler --collection Config --file /data/import/Config.json --jsonArray --mode=upsert || echo "Config import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection SchedulerJob --file /data/import/SchedulerJob.json --jsonArray --mode=upsert || echo "SchedulerJob import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection Users --file /data/import/Users.json --jsonArray --mode=upsert || echo "Users import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection EventDays --file /data/import/EventDays.json --jsonArray --mode=upsert || echo "EventDays import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection Ipo --file /data/import/Ipo.json --jsonArray --mode=upsert || echo "Ipo import 실패"
    mongoimport --host localhost --db ipo-scheduler --collection IpoHistory --file /data/import/IpoHistory.json --jsonArray --mode=upsert || echo "IpoHistory import 실패"
else
    echo "ipo-scheduler 데이터베이스가 이미 존재합니다. Import를 생략합니다."
fi
# MongoDB 프로세스를 백그라운드에서 유지
wait
