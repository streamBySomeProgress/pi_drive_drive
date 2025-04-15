from fastapi import FastAPI
import logging
from log.logger import setup_logger
from router.drive.drive_requestHandler import drive_handler
from router.camera.camera_requestHandler import camera_handler
import uvicorn

app = FastAPI()

# 로깅 설정
logging_info = setup_logger('main', 'log_main.txt', logging.INFO)

app.include_router(drive_handler)
app.include_router(camera_handler)

if __name__ == "__main__":
    logging_info.info("FastAPI server starting...")
    uvicorn.run(app, host="0.0.0.0", port=5000)