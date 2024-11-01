#!/bin/bash
#-------------------------------------------------------
# ipo-scheduler 데이터베이스 백업 스크립트
# /home/kdy987/fastapi/mongodb_backup/20241101/ipo-scheduler 경로에 백업 파일 저장
# 백업 파일은 Config, SchedulerJob, Users, EventDays, Ipo, IpoHistory 컬렉션을 백업
# 백업 파일은 bson 형식으로 저장
# Restoring은 mongo-restore.sh 스크립트를 사용
#-------------------------------------------------------
# 백업 디렉터리 설정 (컨테이너 내부 경로)
BACKUP_DIR="/data/backup/$(date +%Y%m%d)"

# 컨테이너에서 mongodump 명령어 실행하여 각 컬렉션을 백업
docker exec ipo-mongo mongodump --db ipo-scheduler --collection Config --out "$BACKUP_DIR" || echo "Config collection 백업 실패"
docker exec ipo-mongo mongodump --db ipo-scheduler --collection SchedulerJob --out "$BACKUP_DIR" || echo "SchedulerJob collection 백업 실패"
docker exec ipo-mongo mongodump --db ipo-scheduler --collection Users --out "$BACKUP_DIR" || echo "Users collection 백업 실패"
docker exec ipo-mongo mongodump --db ipo-scheduler --collection EventDays --out "$BACKUP_DIR" || echo "EventDays collection 백업 실패"
docker exec ipo-mongo mongodump --db ipo-scheduler --collection Ipo --out "$BACKUP_DIR" || echo "Ipo collection 백업 실패"
docker exec ipo-mongo mongodump --db ipo-scheduler --collection IpoHistory --out "$BACKUP_DIR" || echo "IpoHistory collection 백업 실패"

echo "백업 완료! 호스트의 /home/kdy987/fastapi/mongodb_backup에 백업 파일이 저장되었습니다."
