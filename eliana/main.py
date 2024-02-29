from fastapi import FastAPI, HTTPException
import uvicorn
from matplotlib import pyplot as plt
import base64
from io import BytesIO
from ChartRequest import ChartRequest  # ChartRequest 클래스 임포트

app = FastAPI()

@app.post("/test")
def create_chart(request: ChartRequest):  # 매개변수 타입을 ChartRequest로 변경
    try:
        # 차트 생성
        plt.figure(figsize=(request.width / 100, request.height / 100))
        plt.plot(request.x, request.y)
        plt.title("Sample Chart")

        # 이미지를 Base64 문자열로 변환
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png')
        plt.close()
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')

        return {"image": f"data:image/png;base64,{img_base64}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8989)
