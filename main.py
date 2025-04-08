from fastapi import FastAPI, HTTPException
import threading
import logging

app = FastAPI()

@app.get("/start")
async def start_camera():
    """카메라 시작 엔드포인트"""
    global camera_running, thread
    if not camera_running:
        camera_running = True
        thread = threading.Thread(target=camera_loop)
        thread.start()
        logging.info("Camera started via HTTP")
        return {"message": "Camera started"}
    raise HTTPException(status_code=400, detail="Camera already running")

@app.get("/stop")
async def stop_camera():
    """카메라 종료 엔드포인트"""
    global camera_running, thread
    if camera_running:
        camera_running = False
        thread.join()
        thread = None
        logging.info("Camera stopped via HTTP")
        return {"message": "Camera stopped"}
    raise HTTPException(status_code=400, detail="Camera not running")

@app.get("/status")
async def status():
    """카메라 상태 확인"""
    return {"camera_running": camera_running}