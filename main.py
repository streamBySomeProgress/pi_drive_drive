from fastapi import FastAPI, HTTPException
import threading
import logging
from camera.sampling_eval import camera_loop, camera_loop_abort
from log.logger import setup_logger
from camera.sampling_collect import camera_capture
from router.drive.drive_requestHandler import drive_handler

app = FastAPI()

# 로깅 설정
logging_info = setup_logger('main', 'log_main.txt', logging.INFO)

# 전역 변수
camera_running = False
thread = None

app.include_router(drive_handler)

# todo 하단 핸들러들은 적절히 이동시키거나 삭제
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