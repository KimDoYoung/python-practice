# CentOS 기반 이미지
FROM centos:7

# Python 설치
RUN yum install -y python3 python3-pip && \
    yum clean all

# 작업 디렉토리 설정
WORKDIR /app

# 프로젝트 파일 복사
COPY . /app

# Python 패키지 설치
RUN pip3 install --no-cache-dir -r /app/make_thumb/requirements.txt \
    && pip3 install --no-cache-dir -r /app/ap_file_wh/requirements.txt \
    && pip3 install --no-cache-dir -r /app/hdd/requirements.txt

# 기본 실행 쉘 지정
CMD ["bash"]
