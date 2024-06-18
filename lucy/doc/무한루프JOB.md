# 무한루프로 JOB을 수행시키

## 개요

- 주식매매 전략을 수행하는 데몬같은 프로세스
- 브라우저에서 1. Start, 2.stop, 3.status 를 알아야 한다

## 프롬프트

질문

1. 백그라운드 작업으로 무한루프의 작업을 시키고 임시로 그 작업의 이름을 job1이라고 함
def job1
  while true:
    ...

2. client로부터 request를 받아서 작업을 종료시킬 수 있는가?
3. 그 작업을 다시 시작시킬 수 있는가?
4. 그 작업이 돌고 있다는 것을 알 수 있는가?

## 코드

무한루프의 백그라운드 작업을 실행하려면
**concurrent.futures의 ThreadPoolExecutor**
**asyncio의 create_task**를 사용할 수 있습니다.
여기서는 ThreadPoolExecutor를 사용한 예를 들어보겠습니다.

*job

```python
import time
import threading

# 전역 변수 설정
job1_running = False
job1_thread = None

def job1():
    global job1_running
    while job1_running:
        print("작업 수행 중...")
        time.sleep(1)  # 실제 작업을 대체하는 지연

```

*router

```python
from fastapi import FastAPI
from pydantic import BaseModel
import threading

app = FastAPI()

# 백그라운드 작업을 제어할 수 있는 전역 변수
job1_running = False
job1_thread = None

class JobControl(BaseModel):
    action: str  # 'start' or 'stop'

@app.post("/control_job")
def control_job(control: JobControl):
    global job1_running, job1_thread

    if control.action == "start" and not job1_running:
        job1_running = True
        job1_thread = threading.Thread(target=job1)
        job1_thread.start()
        return {"message": "job1 started"}
    elif control.action == "stop" and job1_running:
        job1_running = False
        if job1_thread is not None:
            job1_thread.join()
        return {"message": "job1 stopped"}
    else:
        return {"message": "invalid action or job already in desired state"}

@app.get("/status")
def status():
    return {"job1_running": job1_running}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

```

- client

```html
<!DOCTYPE html>
<html>
<head>
    <title>Job Control</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <button id="start-button">Start Job</button>
    <button id="stop-button">Stop Job</button>
    <div id="status"></div>

    <script>
        $(document).ready(function() {
            $('#start-button').click(function() {
                fetch('/control_job', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ action: 'start' })
                }).then(response => response.json())
                .then(data => {
                    console.log(data);
                    $('#status').text(data.message);
                });
            });

            $('#stop-button').click(function() {
                fetch('/control_job', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ action: 'stop' })
                }).then(response => response.json())
                .then(data => {
                    console.log(data);
                    $('#status').text(data.message);
                });
            });

            function checkStatus() {
                fetch('/status')
                .then(response => response.json())
                .then(data => {
                    $('#status').text('Job1 running: ' + data.job1_running);
                });
            }

            setInterval(checkStatus, 1000); // 1초마다 상태 체크
        });
    </script>
</body>
</html>

```
