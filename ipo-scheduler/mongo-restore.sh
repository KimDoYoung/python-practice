#!/bin/bash
#-------------------------------------------------------
# ipo-scheduler 데이터베이스 복원 스크립트
# /home/kdy987/fastapi/mongodb_backup/20241101/ipo-scheduler 경로에 백업 파일에서 복원
# 백업 파일은 Config, SchedulerJob, Users, EventDays, Ipo, IpoHistory 컬렉션을 복원
# 백업 파일은 bson 형식으로 저장
# 백업 파일은 mongo-backup.sh 스크립트로 생성
#-------------------------------------------------------
# 백업 경로 설정
BACKUP_DIR="/home/kdy987/fastapi/mongodb_backup/20241101/ipo-scheduler"

# 복원 실행 (각 컬렉션 별로 복원)
docker exec ipo-mongo mongorestore --db ipo-scheduler --collection Config "$BACKUP_DIR/Config.bson"
docker exec ipo-mongo mongorestore --db ipo-scheduler --collection EventDays "$BACKUP_DIR/EventDays.bson"
docker exec ipo-mongo mongorestore --db ipo-scheduler --collection Ipo "$BACKUP_DIR/Ipo.bson"
docker exec ipo-mongo mongorestore --db ipo-scheduler --collection IpoHistory "$BACKUP_DIR/IpoHistory.bson"
docker exec ipo-mongo mongorestore --db ipo-scheduler --collection SchedulerJob "$BACKUP_DIR/SchedulerJob.bson"
docker exec ipo-mongo mongorestore --db ipo-scheduler --collection Users "$BACKUP_DIR/Users.bson"

echo "복원이 완료되었습니다."
