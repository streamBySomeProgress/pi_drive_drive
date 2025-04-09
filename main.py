from fastapi import FastAPI, HTTPException
import threading
import logging
from camera.sampling import camera_loop, camera_loop_abort
from log.logger import setup_logger

# 로깅 설정
logging_info = setup_logger('main', 'log_main.txt', logging.INFO)

# 전역 변수
app = FastAPI()
camera_running = False
thread = None

@app.get("/start")
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

@app.get("/stop")
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

@app.get("/")
async def index():
    """기본 페이지"""
    return {"message": "Camera Control: Use /start or /stop"}

@app.get("/status")
async def status():
    """카메라 상태 확인"""
    return {"camera_running": camera_running}

if __name__ == "__main__":
    import uvicorn
    logging_info.info("FastAPI server starting...")
    uvicorn.run(app, host="0.0.0.0", port=5000)