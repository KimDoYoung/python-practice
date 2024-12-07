FROM ubuntu:20.04

RUN apt update && apt install -y python3 python3-pip && \
    apt clean

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r /app/make_thumb/requirements.txt \
    && pip3 install --no-cache-dir -r /app/ap_file_wh/requirements.txt \
    && pip3 install --no-cache-dir -r /app/hdd/requirements.txt

CMD ["bash"]
