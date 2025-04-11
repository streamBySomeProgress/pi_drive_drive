from fastapi import FastAPI, HTTPException
import threading
import logging
from camera.sampling_eval import camera_loop, camera_loop_abort
from log.logger import setup_logger
from camera.sampling_collect import camera_capture
from torchArea.cnn.lineCnn import LineCNN

# 로깅 설정
logging_info = setup_logger('main', 'log_main.txt', logging.INFO)

# 전역 변수
app = FastAPI()
camera_running = False
thread = None

# 모델 초기화
model = LineCNN()

@app.get("/")
async def index():
    """기본 페이지"""
    return {"message": "Camera Control: Use /sampling/start or /sampling/stop"}

# todo 추후 실 주행 테스트 할 시 카메라 영역은 main 영역에서 별도 영역으로 이동시켜야
@app.get("/sampling/start")
async def start_camera():
    """카메라 시작 엔드포인트"""
    global camera_running, thread
    if not camera_running:
        camera_running = True
        thread = threading.Thread(target=camera_loop)
        thread.start()
        logging_info.info("Camera started via HTTP")
        return {"message": "Camera started"}
    raise HTTPException(status_code=400, detail="Camera already running")

@app.get("/sampling/stop")
async def stop_camera():
    """카메라 종료 엔드포인트"""
    global camera_running, thread
    if camera_running:
        camera_running = False
        camera_loop_abort() # 중단
        thread.join() # camera_loop 를 실행하는 스레드가 중단될 때까지 대기
        thread = None # 할당 해제
        logging_info.info("Camera stopped via HTTP")
        return {"message": "Camera stopped"}
    raise HTTPException(status_code=400, detail="Camera not running")

@app.get("/sampling/status")
async def status():
    """카메라 상태 확인"""
    return {"camera_running": camera_running}

@app.get("/capture")
async def capture_frame(class_label: int = None):
    global frame_count, camera_running
    if not camera_running:
        raise HTTPException(status_code=400, detail="Camera is not running. Start it first with /start")
    if not 0 <= class_label <= 5:
        raise HTTPException(status_code=400, detail="class_label must be between 0 and 5")

    filepath, prediction = camera_capture(class_label)

    position_map = {0: "Left", 1: "Center", 2: "Right", 3: "None", 4: "Left Curve", 5: "Right Curve"}
    return {"message": f"Frame captured and saved as {filepath}", "prediction": position_map[prediction], "label_used": class_label}

if __name__ == "__main__":
    import uvicorn
    logging_info.info("FastAPI server starting...")
    uvicorn.run(app, host="0.0.0.0", port=5000)